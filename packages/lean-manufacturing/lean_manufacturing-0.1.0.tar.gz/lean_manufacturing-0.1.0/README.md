# Lean manufacturing for Python
* Use lean manufacturing concepts to streamline python workflow. 
* Organize and access your workflow through a mongodb local installation.
* Make your relevant functions independent from each other.
* Configure and make adjustments to your functions through mongodb.

## Requirements

You'll need a localhost default installation of the community version of MongoDb (i.e. accessible at *mongodb://localhost:27017*).

This is a great and easy-to-use database, completely free. Please see https://www.mongodb.com/docs/manual/installation/ if you need help with the installation.

### Not required, but useful

Mongodb Compass is a free software from mongodb that allows you to visually edit your mongodb databases. Please see https://www.mongodb.com/products/compass if you wants to download it.

## Usage

### Simple use

For usage, simply include a decorator to your main functions, and make sure to include **config as key arguments to your function.

```
from lean-manufacturing import Lean

@Lean.production_line('my_first_production_line')
def do_something_relevant(**config):

    # get elements from somewhere
    elements = [{'_id': a, number: 1}, {'_id': b, number: 2}]

    # do something with the elements
    processed_elements = [{'_id': element['_id'], number= element['number']*2 } for element in elements]

    # return elements
    return processed_elements

```
Lean will automatically save the output to the 'workers' database under the collection name 'my_first_production_line.do_something_relevant'.

### Getting output from other functions

If you need to call the output of a function in another function, you can use the 'workers_db'.

```
from lean-manufacturing import Lean

@Lean.production_line('my_first_production_line')
def another_function(**config):

    workers_db = config.get('workers_db')

    # get elements using mongodb operators
    elements = workers_db['my_first_production_line.another_function'].find()

    # do something with the elements
    processed_elements = [{'_id': element['_id'], number= element['number']*2 } for element in elements]

    # return elements
    return processed_elements

```

Remember that lean will automatically save the output to the 'workers' database under the collection name 'my_first_production_line.another_function'.

### Getting custom parameters for configuring your functions

Lean creates and mantains a document for each worker at a local db named 'monitor' under a collection named 'workers' (do not confuse with the db named 'workers' which stores the output from functions).

This will automatically store very interesting data about the functions, such as the 'last_duration', the 'last_success', the 'last_failure' and a list of errors with the 'error_time' and 'message'.

You can also store custom configuration data, which will be accessible through the 'config' dictionary.

In the following example, assume that you have manually include a 'my_key_at_mongodb' at your function's document at mongodb.

```
from lean-manufacturing import Lean

@Lean.production_line('my_first_production_line')
def my_configured_function(**config):

    my_config_variable = config.get('my_key_at_mongodb')

    # get elements from somewhere
    elements = [{'_id': a, number: 1}, {'_id': b, number: 2}]

    # do something with the elements
    processed_elements = [{'_id': element['_id'], number= element['number']*my_config_variable } for element in elements]

    # return elements
    return processed_elements

```
Remember that lean will automatically save the output to the 'workers' database under the collection name 'my_first_production_line.my_configured_function'.

### Bonus

You'll also get a Lean.log function with all python default logging operators, that will automatically store your logs to the db named 'monitor', at the collection named 'logs'.

```
from lean-manufacturing import Lean

Lean.log.critical('This is a critical logging')
Lean.log.error('This is an error logging')
Lean.log.warning('This is a warning logging')
Lean.log.info('This is an info logging')
Lean.log.debug('This is a debug logging')

```

## Inspiration and underlying concepts

**SIPOC** means Suppliers, Input Requirements, Process, Output Requirements and Clients. Each function should have a clear SIPOC. 

**Repository** means the common packages accessible from all applications.

**Building Blocks** means the idea of creating small independent functions with clear SIPOC which form an application.

**Production Line** means a group of processes with the final output of a Finished Good.

**Finished Good** means an output with value to the final client.

**Raw Materials** means the input for a process.

**Work in Progress** means the status of some work from the moment the first process of the production line has started to the moment it becomes a Finished Good.

**Lead Time** means the period of time from the moment the ticket has been created to the moment it becomes a Finished Good.

**Process Time** means the period of time from the moment a process has been initiated to the moment the process has ended.

**Total Output Processed** means the total output of a Production Line.

**Total Daily Output** means the total output of a Production Line in the last 24h.

**Average Lead Time** means the average Lead Time of the Finished Goods of the processes in a given Production Line in the last 24h.

**Monitoring System** mean the visual interface for accompanying the status of events, logs and metrics, with event router to store, graph or alert. Should contain the time of the last success, last failure and last duration of each worker.

**Managing DB** means the database that controls the production line, the workers, events, logs and metrics.

**Production DB** means the database with the Finished Goods.

## Simple is better than complex

This is a 75-lines code, including all newlines necessary to make it also beautiful (beautiful is better than ugly). In fact, this markdown is larger than the code.