import enum
import os
from qiboconnection.config import logger

import asyncio

logger.setLevel('DEBUG')
from qiboconnection.connection import ConnectionConfiguration
import numpy as np
from qiboconnection.api import API

import time

from qibo.gates import X, M
from qibo.models.circuit import Circuit
circuit = Circuit(nqubits=1)
circuit.add(X(0))
circuit.add(M(0))

class DebugEnvironment(str, enum.Enum):
    """ Quick class for doing a switch of the backend server """
    DEV="DEV"
    PROD="PROD"

DEBUG_ENV=DebugEnvironment.PROD

if DEBUG_ENV == DebugEnvironment.DEV:
    os.environ["QIBOCONNECTION_ENVIRONMENT"] = 'development'
    connection_bsc = API(configuration=ConnectionConfiguration(username="bsc-user", api_key="bsc-user"))
    connection = API(configuration=ConnectionConfiguration(
        username="qili-admin-test",
        api_key="45843bfc-c404-42ad-abc5-070dk7869420",
    ))

if DEBUG_ENV == DebugEnvironment.PROD:
    os.environ["QIBOCONNECTION_ENVIRONMENT"] = 'staging'
    configuration = ConnectionConfiguration(
        username="qili-admin-test",
        api_key="d31d38f4-228e-4898-a0a4-4c4139d0f79f",
    )
    connection = API(configuration=configuration)

connection.ping()
connection.select_device_ids([1])
ids = connection.execute(circuit=circuit, nshots=1)
connection.list_devices()

print("la primnera, con patatas")
try:
    connection_bsc.select_device_id(10)
except:
    print("la segunda ha peato")

ids = []
for i in range(2):
    connection.select_device_id(device_id=1)
    ids.append(connection.execute(circuit=circuit))


# HEATMAP ONE POINT IN TIME; X SCANNING
x_list = np.linspace(start=0, stop=1, num=100)
y_list = np.linspace(start=0, stop=0.1, num=100)

devices = connection.list_devices()
print(devices)
connection.select_device_id(device_id=1)
connection.get_results( connection.execute(circuit=circuit) )

df0 = connection.list_saved_experiments(favourites=False).dataframe
df1 = connection.list_runcards()
ru0 = connection.get_runcard(runcard_name="sauron_cluster")
ex0 = connection.get_saved_experiments(saved_experiment_ids=[43, 32])
pass


async def main():
    """main"""

    plot_id_rows = await connection.create_liveplot(
        plot_type='SCATTER',
        title='$$\\mathbf{P}((X,Y) \\in B) = \\mathop{\\int\\int}\\limits_{(x,y) \\in B} \\otimes_{i=0}^N \\frac{f^i_{X,Y}(x,y)}{g^i_{X,Y}(x,y)} \\,dx \\,dy \\forall f,g$$',
        y_label='$$\sqrt{\\frac{cool}{what}}$$',
        x_label='$$\\frac{cool}{\hat{hat}}$$',
        z_label='NO latex here',
        x_axis=x_list,
        y_axis=y_list)

    plot_id_rows_3 = await connection.create_liveplot(
        plot_type='HEATMAP',
        title='$$\\mathbf{P}((X,Y) \\in B) = \\mathop{\\int\\int}\\limits_{(x,y) \\in B} \\otimes_{i=0}^N \\frac{f^i_{X,Y}(x,y)}{g^i_{X,Y}(x,y)} \\,dx \\,dy \\forall f,g$$',
        y_label='$$\sqrt{\\frac{cool}{what}}$$',
        x_label='$$\\frac{cool}{\hat{hat}}$$',
        z_label='NO latex here',
        x_axis=x_list,
        y_axis=y_list)

    for Y in y_list:
        for X in x_list:
            Z = float(np.sin(X * Y / (2 * np.pi)))
            await connection.send_plot_points(plot_id=plot_id_rows_3, x=X, y=Y, z=Z)
            await connection.send_plot_points(plot_id=plot_id_rows, x=X, y=Y)
            time.sleep(0.0)


if __name__ == "__main__":
    asyncio.run(main())
    print("Finished. Sleeping")
    time.sleep(30)
    print("Que siestica más buena. Adeu")

