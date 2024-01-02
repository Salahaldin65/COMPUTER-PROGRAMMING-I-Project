import csv

def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            record = {}
            for i in range(len(header)):
                record[header[i]] = row[i]
            data.append(record)
    return data

def calculate_indicators(data):
    for i in range(4, len(data)):
        sma_sum = 0
        for j in range(i - 4, i + 1):
            sma_sum += float(data[j]['Close'])
        data[i]['SMA'] = sma_sum / 5

    for i in range(14, len(data)):
        gains = 0
        losses = 0
        for j in range(i - 13, i):
            change = float(data[j + 1]['Close']) - float(data[j]['Close'])
            if change > 0:
                gains += change
            else:
                losses += abs(change)
        avg_gain = (float(data[i - 1]['AvgGain']) * 13 + gains) / 14
        avg_loss = (float(data[i - 1]['AvgLoss']) * 13 + losses) / 14
        relative_strength = avg_gain / avg_loss
        data[i]['RSI'] = 100 - (100 / (1 + relative_strength))
        data[i]['AvgGain'] = avg_gain
        data[i]['AvgLoss'] = avg_loss

def write_to_file(data, indicator, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', indicator])
        for i in range(14, len(data)):
            writer.writerow([data[i]['Date'], data[i][indicator]])

file_path = 'orcl.csv'
financial_data = load_data(file_path)
financial_data[0]['AvgGain'] = financial_data[0]['AvgLoss'] = 0
for i in range(1, 14):
    change = float(financial_data[i]['Close']) - float(financial_data[i - 1]['Close'])
    if change > 0:
        financial_data[i]['AvgGain'] = change
        financial_data[i]['AvgLoss'] = 0
    else:
        financial_data[i]['AvgGain'] = 0
        financial_data[i]['AvgLoss'] = abs(change)

calculate_indicators(financial_data)
write_to_file(financial_data, 'SMA', 'orcl-sma.csv')
write_to_file(financial_data, 'RSI', 'orcl-rsi.csv')


