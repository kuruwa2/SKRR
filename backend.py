import hashlib
import json
from verify import verify
from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
  status = {'status': 0}
  data = request.get_json(silent=True)
  print('login!')
  totalTime = data['interval'][-1]
  interval = data['interval']
  interval = [0]+[interval[i+1]-interval[i] for i in range(len(interval)-1)]
  intervalScale = [i/totalTime for i in interval]
  hash = hashlib.sha256()
  hash.update(data['pwd'].encode('utf-8'))
  pwd = ''
  try:
    with open('./account/'+data['acc'], 'r') as f:
      pwd = f.readlines()[1][:-1]
      print(hash.hexdigest())
      print(pwd)
  except:
    print('failed: acc')
    return json.dumps(status)
  if hash.hexdigest() != pwd:
    print('failed: pwd')
    return json.dumps(status)
  print(data['acc'])
  if verify(intervalScale, data['acc'])==-1:
    print('failed: habit')
    return json.dumps(status)

  with open('./account/'+data['acc'], 'a') as f:
    f.write(','.join(str(i) for i in intervalScale)+'\n')

  print(f'total time: {totalTime}')
  print(f'interval: {interval}')
  print(f'interval scale: {intervalScale}')
  status['status'] = 1
  return json.dumps(status)

@app.route('/signup', methods=['POST'])
def signup():
  print('signup!')
  data = request.get_json(silent=True)
  print(data)
  totalTime = [i[-1] for i in data['intervalPwd']]
  print(totalTime)
  interval = data['intervalPwd']
  print(interval)
  interval = [[0]+[i[j+1]-i[j] for j in range(len(i)-1)] for i in interval]
  print(interval)
  intervalScale = [[v[j]/totalTime[i] for j in range(len(v))] for i, v in enumerate(interval)]
  print(intervalScale)
  hash = hashlib.sha256()
  hash.update(data['pwd'].encode('utf-8'))
  with open('./account/'+data['acc'], 'w') as f:
    f.write(data['acc']+'\n')
    f.writelines(hash.hexdigest()+'\n')
    for i in intervalScale:
      f.write(','.join(str(j) for j in i)+'\n')
  return data

@app.route('/success')
def success():
  return render_template('success.html')

@app.route('/fastLogin')
def fastLogin():
  return render_template('fastlogin.html')

@app.route('/fastlogin', methods=['POST'])
def fastlogin():
  status = {'status': 0}
  data = request.get_json(silent=True)
  print('login!')
  totalTime = data['interval'][-1]
  interval = data['interval']
  interval = [0]+[interval[i+1]-interval[i] for i in range(len(interval)-1)]
  intervalScale = [i/totalTime for i in interval]
  hash = hashlib.sha256()
  hash.update(data['pwd'].encode('utf-8'))
  pwd = ''
  try:
    with open('./account/'+data['acc'], 'r') as f:
      pwd = f.readlines()[1][:-1]
      print(hash.hexdigest())
      print(pwd)
  except:
    print('failed: acc')
    return json.dumps(status)
  if hash.hexdigest() != pwd:
    print('failed: pwd')
    return json.dumps(status)
  print(data['acc'])

  with open('./account/'+data['acc'], 'a') as f:
    f.write(','.join(str(i) for i in intervalScale)+'\n')

  print(f'total time: {totalTime}')
  print(f'interval: {interval}')
  print(f'interval scale: {intervalScale}')
  status['status'] = 1
  return json.dumps(status)

if __name__ == '__main__':
  app.debug = True
  app.run()
