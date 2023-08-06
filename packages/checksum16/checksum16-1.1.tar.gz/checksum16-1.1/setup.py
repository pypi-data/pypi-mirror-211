from distutils.core import setup, Extension

def build():
    with open('README.md', 'rt') as f:
        long_description = f.read()

    checksum_module = Extension('checksum', 
            sources = ['checksum.c'],
            extra_compile_args=['-Wall', '-Wextra',
                '-Wno-missing-field-initializers', '-Werror'],
            extra_link_args=['-Wl,--build-id=none', '-s'])

    setup(name='checksum16',
            version='1.1',
            description='Native checksum implementation for python',
            author='Efi Weiss',
            author_email='valmarelox@gmail.com',
            url='https://github.com/Valmarelox/checksum',
            python_requires='>=3',
            ext_modules = [checksum_module],
            long_description=long_description,
            long_description_content_type='text/markdown')


if __name__ == '__main__':
    build()
