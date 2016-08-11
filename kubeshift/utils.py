class Utils(object):

    @staticmethod
    def sanitizeName(app):
        return app.replace("/", "-").replace(":", "-")
