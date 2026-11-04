# twine_a.py
import twine.__main__
import twine.repository


def disable_server_certificate_validation():
    """
    Disable SSL verification for all twine uploads
    :return:
    """
    old_init = twine.repository.Repository.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    twine.repository.Repository.__init__ = new_init


def main():
    disable_server_certificate_validation()
    twine.__main__.main()


if __name__ == '__main__':
    main()