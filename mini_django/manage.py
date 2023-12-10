from mini_django.core.managements.commands.runserver import RunServer

if __name__ == '__main__':
    run_server = RunServer()
    run_server.run(True, "0", 81, True)
