from app import app, isValidPath

if isValidPath():

    if __name__ == '__main__':
        import waitress
        waitress.serve(app, host='0.0.0.0', port=8000)