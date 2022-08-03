import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def get_plot(chat_id: int, pressure_data: list, file_name: str) -> bytes:
    data_for_plot = {
        'date': [(datetime.fromisoformat(line[1]) + timedelta(hours=3)).strftime('%Y-%m-%d\n%H-%M-%S')
                 for line in pressure_data
                 if line[0] == chat_id],
        'systolic_pressure': [line[2] for line in pressure_data if line[0] == chat_id],
        'diastolic_pressure': [line[3] for line in pressure_data if line[0] == chat_id],
        'pulse': [line[4] for line in pressure_data if line[0] == chat_id]
    }

    plt.figure(figsize=(20, 20))
    plt.plot(data_for_plot['date'], data_for_plot['systolic_pressure'], label='systolic pressure', markeredgewidth=5)
    plt.plot(data_for_plot['date'], data_for_plot['diastolic_pressure'], label='diastolic pressure', markeredgewidth=5)
    plt.plot(data_for_plot['date'], data_for_plot['pulse'], label='pulse', markeredgewidth=5)
    plt.legend()
    plt.savefig(file_name)
    with open(file_name, 'rb') as f:
        return f.read()
