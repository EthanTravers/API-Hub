import azure.functions as func

app = func.FunctionApp()
bp = func.Blueprint("test")
error = "..."


app.register_blueprint(bp)

try:

    from functions.player.player_login import function as player_login
    from functions.player.player_register import function as player_register

    function_list = [
        player_login,
        player_register
    ]

    for function in function_list:
        app.register_blueprint(function)


except Exception as e:
    import logging
    error = str(e)
