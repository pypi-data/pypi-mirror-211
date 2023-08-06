# RapidExec (Work in progress)

RapidExec is a command line tool that allows you to easier access docker containers. It is written in Python and uses the docker API to interact with the containers.


## Installation

1. To install RapidExec with all dependencies, you can use the following command:

    ```bash
    pip install rapidexec
    ```

2. To install RapidExec with only export dependencies, you can use the following command:
   
    ```bash
    pip install rapidexec[export]
    ```

3. To install RapidExec with only docker dependencies, you can use the following command:
   
    ```bash
    pip install rapidexec[docker]
    ```
   

## Usage

To use RapidExec, you can use the following command:

```bash
rapidexec [OPTIONS] COMMAND [ARGS]...
```

### Options

| Option    | Description                |
|-----------|----------------------------|
| --help    | Shows usage information    |
| --version | Show the version and exit. |

### Commands

| Command      | Description                                                    |
|--------------|----------------------------------------------------------------|
| docker-ps    | List all running containers.                                   |
| docker-logs  | Show the logs of a container.                                  |
| compose-logs | Show the logs of a docker-compose service.                     |
| export       | Export pyproject.toml dependencies to a requirements.txt file. |


### Example output

#### docker-ps
```bash
$ rapidexec docker-ps
```
![image](https://raw.githubusercontent.com/godd0t/rapidexec/main/docs/images/docker-ps.png)

#### export

1. Scenario: toml file pyproject.toml and output file requirements.txt
    ```bash
    $ rapidexec export -f pyproject.toml -o requirements.txt
    ```
    ![image](https://raw.githubusercontent.com/godd0t/rapidexec/main/docs/images/export.png)

2. Scenario: exclude optional groups
    ```bash
    $ rapidexec export --exclude dev,export
    ```
    ![image](https://raw.githubusercontent.com/godd0t/rapidexec/main/docs/images/export-exclude.png)
3. Scenario: include only specific optional groups
    ```bash
    $ rapidexec export --include dev
    ```
    ![image](https://raw.githubusercontent.com/godd0t/rapidexec/main/docs/images/export-include.png)


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/godd0t/rapidexec/blob/main/LICENSE) file for details.


## Contributing

If you want to contribute to this project, you can create a pull request on GitHub.
