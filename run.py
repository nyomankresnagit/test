from app import create_app
# from docs.docs import app

if __name__ == '__main__':
    app = create_app()
    app.run()

    # app.run()