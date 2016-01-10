from distutils.core import setup

setup(
    name='PyPong',
    version='0.1',
    packages=[
        'Assets',
        'Systems',
        'Systems/Engine',
        'Systems/Game',
        'Systems/Network',
        'Systems/Network/Messages',
        'Systems/Network/tcp',
        'Systems/Scenes',
        'Systems/Scenes/Gameplay',
        'Systems/Scenes/NetworkLobby',
        'Systems/Utils',
        'Tests'
    ],
    data_files=[
        ('', [
            'LICENSE',
            'README.md',
            'Assets/ball.jpg'
        ])
    ],
    url='https://github.com/RippeR37/PyPong',
    license='',
    author="RippeR37",
    description='Multiplayer Pong game in Python.',
    py_modules=['PyPong', 'PyPongStandaloneServer']
)
