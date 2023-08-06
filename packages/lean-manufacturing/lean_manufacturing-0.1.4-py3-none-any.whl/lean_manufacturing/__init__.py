from datetime import datetime
import pymongo
import logging


localdb = pymongo.MongoClient('mongodb://localhost:27017')

class Lean:
    @classmethod
    def _start(cls):
        cls.management_db               = localdb
        cls.log                         = logging.getLogger('logs')

        cls.log.addHandler(_MongoHandler())

    def production_line(production_line, **dwargs):
        def wrapper(func):
            def applicator(*args, **kwargs):
                collection_name         = f'{production_line}.{func.__name__}'
                create_event            = Lean.management_db['monitor']['events'].insert_one({'collection': collection_name, 'action': f'Started {production_line}: {func.__name__}', 'at': datetime.now()})
                turn_worker_on          = Lean.management_db['monitor']['workers'].update_one({'collection': collection_name, 'name': func.__name__, 'production_line': production_line}, {'$set': {'running': True}}, upsert=True)

                try:
                    initial_time                = datetime.now()
                    worker_config               = Lean.management_db['monitor']['workers'].find_one({'name': func.__name__, 'production_line': production_line})
                    kwargs['workers_db']        = Lean.management_db['workers']
                    kwargs['monitor_db']        = Lean.management_db['monitor']
                    kwargs['collection_name']   = collection_name
                    
                    kwargs              = kwargs | worker_config if worker_config else kwargs
                    result              = func(*args, **kwargs)
                    if result:
                        documents_to_update = [document for document in result if '_id' in document if type(result) == list]
                        documents_to_insert = [document for document in result if '_id' not in document if type(result) == list]
                        bulk_update         = Lean.management_db['workers'][collection_name].bulk_write([pymongo.UpdateOne({'_id': document['_id']}, {'$set': document}, upsert=True) for document in documents_to_update if documents_to_update]).bulk_api_result if documents_to_update else None
                        bulk_insert         = Lean.management_db['workers'][collection_name].insert_many(documents_to_insert).inserted_ids if documents_to_insert else None
                        duration            = datetime.now() - initial_time
                        turn_worker_off     = Lean.management_db['monitor']['workers'].update_one({'collection': collection_name, 'name': func.__name__, 'production_line': production_line}, {'$set': {'running': False, 'last_success': datetime.now(), 'last_duration': duration.microseconds}}, upsert=True)
                        
                        Lean.log.info(bulk_update)
                        Lean.log.info(bulk_insert)
                    return result

                except Exception as e:
                    error_time          = datetime.now()
                    error_message       = str(e).partition('\n')[-1]
                    Lean.log.error(error_message)
                    turn_worker_off     = Lean.management_db['monitor']['workers'].update_one({'collection': collection_name, 'name': func.__name__, 'production_line': production_line}, {'$set': {'running': False, 'last_failure': error_time}, '$addToSet': {'errors': {'error_time': error_time,'message': error_message}}}, upsert=True)
                    raise
            return applicator
        return wrapper

    def setup(**dwargs):
        collection_name             = dwargs.get('collection_name', None)
        if not collection_name:
            raise
        def wrapper(func):
            def applicator(*args, **kwargs):
                initial_time                = datetime.now()
                result              = func(*args, **kwargs)
                duration            = datetime.now() - initial_time
                update_duration     = Lean.management_db['monitor']['workers'].update_one({'collection': collection_name}, {'$set': {'last_setup': datetime.now(), 'last_setup_duration': duration.microseconds}}, upsert=True)
                return result
            return applicator
        return wrapper

    def process(**dwargs):
        collection_name             = dwargs.get('collection_name', None)
        if not collection_name:
            raise
        def wrapper(func):
            def applicator(*args, **kwargs):
                initial_time                = datetime.now()
                result              = func(*args, **kwargs)
                duration            = datetime.now() - initial_time
                update_duration     = Lean.management_db['monitor']['workers'].update_one({'collection': collection_name}, {'$set': {'last_process': datetime.now(), 'last_process_duration': duration.microseconds}}, upsert=True)
                return result
            return applicator
        return wrapper


class _MongoHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET, database='monitor', collection='logs', capped=True, size=100000, drop=False):
        logging.Handler.__init__(self, level)

        self.database                   = localdb[database]

        if collection in self.database.list_collection_names():
            if drop:
                self.database.drop_collection(collection)
                self.collection         = self.database.create_collection(collection, **{'capped': capped, 'size': size})
            else:
                self.collection         = self.database[collection]
        else:
            self.collection             = self.database.create_collection(collection, **{'capped': capped, 'size': size})

    def emit(self, record):
        log_content = {'when': datetime.now(),
                    'levelno': record.levelno,
                    'levelname': record.levelname,
                    'message': record.msg}
        self.collection.insert_one(log_content)
        print('{when} - {levelname} - {levelno} - {message}'.format(**log_content))
        
Lean._start()