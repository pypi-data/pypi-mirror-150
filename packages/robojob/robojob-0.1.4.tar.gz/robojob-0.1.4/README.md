
# Configuration file schema

- `environment`: The name of the environment if none is supplied, this defaults to the host name (as defined by `socket.gethostname()`)
- `path`: A list of paths that will be appended to the path environment variable


# Backend interface

The following methods will be called 

- `before_job_execution(job_execution)`: Called before any tasks or orchestration code is called. Must assign a value to the `id` property of the job execution.

- `before_task_execution(job_execution, task_execution)`: Called right before each task is executed. Must assign a value to the `id` property of the task execution.