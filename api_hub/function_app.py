import azure.functions as func

app = func.FunctionApp()
bp = func.Blueprint("test")
error = "..."


app.register_blueprint(bp)

try:

    from functions.user.user_login import function as user_login
    from functions.user.user_register import function as user_register
    from functions.user.user_delete import function as user_delete

    function_list = [
        user_login,
        user_register,
        user_delete
    ]

    for function in function_list:
        app.register_blueprint(function)


except Exception as e:
    import logging
    error = str(e)
