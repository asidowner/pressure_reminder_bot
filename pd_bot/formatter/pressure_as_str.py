from datetime import datetime, timedelta


def pressure_as_str(chat_id: int, pressure_data: list):
    result: list = []
    for line in pressure_data:
        if line[0] == chat_id:
            date = datetime.fromisoformat(line[1]) + timedelta(hours=3)
            systolic_pressure = line[2]
            diastolic_pressure = line[3]
            pulse = line[4]
            result.append(f'{date} - {systolic_pressure}/{diastolic_pressure}, pulse - {pulse}')
    return '\n'.join(result)
