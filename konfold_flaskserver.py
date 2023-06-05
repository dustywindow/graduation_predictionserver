# flask : pip install flask
from flask import Flask
from flask import request, Response

# fasta : pip install biopython
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
# from Bio.Alphabet import generic_protein #1.78에서 Bio.Alphabet 사라짐

# subprocess
import subprocess

# json
import json

# time
from datetime import datetime
now = datetime.now()
start_time = 0
end_time = 0

# Flask 인스터드 생성
app = Flask(__name__)

# Topic List
topics = [{'id':'test', 'title':'test', 'body':'konfold/test'},
          {'id':'alphafold2', 'title':'alphafold2', 'body':'konfold/alphfold2'}]

# 출력 template
def template(content):
    return f'''
            <html>
            <head>
            </head>
            <body>
                {content}
            </body>
            </html>
            '''

# 사용자로부터 입력받은 sequence와 저장할 name을 저장
def get_sequence(seq):
    input_sequence = seq
    now_time = now.strftime("%H-%M")
    input_name = f"predict-{now.date()}-{now_time}"
    return input_sequence, input_name

# 입력받은 sequence를 fasta 파일로 변환(쓰기)
def make_fasta(sequence, name):
    rec1 = SeqRecord(Seq(f'{sequence}'),
                     id=f"{name}",
                     description="")
    my_records = [rec1]
    input_fastapath = f"/minji/protein/alphafold/input/{name}.fasta"
    SeqIO.write(my_records, f'{input_fastapath}', "fasta")
    return input_fastapath

# 입력받은 fasta 파일을 읽기   
def read_fasta(fastapath):
    for seq_record in SeqIO.parse(f"{fastapath}", "fasta"):
         id = seq_record.id
         #seq = repr(seq_record.seq) # Seq('AAA...AAA')형태로 출력
         seq = seq_record.seq
         length = len(seq_record)
    return id, seq, length

# alphafold2 prediction model
def get_prediction(fastapath, name):
    # test용_fasta 읽기
    id, seq, len = read_fasta(fastapath)
    
    #alphafold 실행
    output_dirpath = f"/minji/protein/output"
    output_resultpath = f"{output_dirpath}/{name}/ranked_0.pdb"
    prediction_call = f"python3 /minji/protein/alphafold/docker/run_docker.py --fasta_paths=/minji/protein/alphafold/input/{name}.fasta --max_template_date=2023-04-30 --data_dir=/minji/protein/db/ --model_preset=monomer --db_preset=reduced_dbs --output_dir=/minji/protein/output/"
    result = subprocess.run(prediction_call, shell=True, capture_output=True, text=True)
    
    result = output_resultpath
    
    return result, id, seq, len

# 웹 표현: route() 메소드 사용
# 127.0.0.1:5000 으로 접근 
@app.route("/") 
# 맨 앞에 @가 붙는 것은 장식자(decorator)
# flaks에서는 이러한 장식자가 URL 연결에 활용된다.
# 장식자를 사용하면 다음 행의 함수부터 장식자가 적용된다. 
# 함수코드를 바꾸지 않고 장식자 안의 내용만 바꿈으로 함수의 동작을 조절할 수 있다.
# 플라스크 서버로 '/'URL요청이 들어왔을 때 어떤 함수를 호출할 것인지를 조정

def konfold_start():
    liTags = ''
    # List의 각 토픽의 제목을 <li>로 웹에 출력하기 위해 liTags 변수에 문자열로 저장
    for topic in topics:
        liTags += f'''
                    <li>
                    <a href="/konfold/{topic["id"]}">
                    {topic["title"]}
                    </a>
                    </li>
                    '''
    Hello = f'''
            <h2>
            Konfold Start
            </h2>
            Hello, it's KonFold!
            <ol>
            {liTags}
            </ol>
            '''
    return template(Hello)

# 127.0.0.1:5000/konfold/test 으로 접근 
@app.route("/konfold/test")

def test():
    for topic in topics:
        if(topic["id"] == 'test'):
            # sequence를 전달받음_test용 임의입력
            # A0A009EUU2
            #seq = "MPTFTSNDAQINYQTFGDASKPALVFSNSLGTKYSMWQPQIAHFQQDYYVICYDTRGHGGSEAPQGPYSLEQLGQDVVNLLDHLDIAKAAFCGISMGGLTGQWLAIHKPERFSQVIVCNTAAKIGQEQAWQDRAALVREQGLAPIASTAASRWFTDPFIQSNPAVVAELSNDLGAGSPEGYANCCEALAKADVREQLSSIQIPVLIIAGQQDPVTTVADGQFMQQRIANSQLFEINASHISNIEQPEAFNQAVQTFLAA"
            # 2ZNL_1
            seq = "NGYIEGKLSQMSKEVNARIEPFLKTTPRPLRLPNGPPCSQRSKFLLMDALKLSIEDPSHEGEGIPLYDAIKCMRTFFGWKEPNVVKPHEKGINPNYLLSWKQVLAELQDIENEEKIPKTKNMKKTSQLKWALGENMAPEKVDFDDCKDVGDLKQYDSDEPELRSLASWIQNEFNKACELTDSSWIELDEIGEDVAPIEHIASMRRNYFTSEVSHCRATEYIMKGVYINTALLNASCAAMDDFQLIPMISKCRTKEGRRKTNLYGFIIKGRSHLRNDTDVVNFVSMEFSLTDPRLEPHKWEKYCVLEIGDMLIRSAIGQVSRPMFLYVRTNGTSKIKMKWGMEMRRCLLQSLQQIESMIEAESSVKEKDMTKEFFENKSETWPIGESPKGVEESSIGKVCRTLLAKSVFNSLYASPQLEGFSAESRKLLLIVQALRDNLEPGTFDLGGLYEAIEECLINDPWVLLNASWFNSFLTHALS"
            # 전달된 sequence를 저장
            input_sequence, input_name = get_sequence(seq)
            
            # sequence를 fasta 파일로 저장
            input_fastapath = make_fasta(input_sequence, input_name)
            
            # predict
            print("start predict")
            start = now.timestamp()
                
            # model
            output_result = input_fastapath
            output_id, output_seq, output_len = read_fasta(input_fastapath)
                
            end = now.timestamp()
            result_time = (float)(start-end)
            print("complete")
            print("name: %s\t length: %d\t time: %f" %(output_id, output_len, result_time))
            
            content = f'''
                        <h2>
                        {topic["title"]}
                        </h2>
                        {topic["body"]}<br><br>
                        name : {input_name}<br>
                        sequence : {input_sequence}<br><br>
                        
                        predict time : {result_time}<br>
                        result : {output_result}<br>
                        {output_id},<br> {output_seq},<br> {output_len}<br>
                        '''
    return template(content)

# 127.0.0.1:5000/konfold/predict 으로 접근 
@app.route("/konfold/alphafold2", methods=['POST'])

def alphafold2():
    if request.method == 'POST':
        # sequence를 전달받음
        seq = request.get_json()
        if not seq:
            raise ValueError
                
    for topic in topics:
        if(topic["id"] == 'alphafold2'):
                # 전달된 sequence를 저장
            input_sequence, input_name = get_sequence(seq['proteinName'])
                    
            # sequence를 fasta 파일로 저장
            input_fastapath = make_fasta(input_sequence, input_name)
            
            # predict
            print("start predict")
            start = now.timestamp()
                        
            # model
            output_result, output_id, output_seq, output_len = get_prediction(input_fastapath, input_name)
    
            end = now.timestamp()
            result_time = (float)(start-end)
            print("complete")
            print("name: %s\t length: %d\t time: %f" %(output_id, output_len, result_time))
                                       
            content = f'''
                        <h2>
                        {topic["title"]}
                        </h2>
                        {topic["body"]}<br><br>
                        name : {input_name}<br>
                        sequence : {input_sequence}<br><br>
                        predict time : {result_time}<br>
                        result : {output_result}<br>
                        {output_id},<br> {output_seq},<br> {output_len}<br> 
                        '''       
            
            # result파일 불러오기
            res = {
                "file" : open(f'{output_result}', 'r')
            }

            res = Response(json.dumps(template(res), ensure_ascii=False))
            res.headers['Content-Type'] = 'application/json'
                
            return res

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
    # 플라스크는 localhost라고 알려진 루프백 주소 127.0.0.1을 사용: IP와 관계없이 내 컴퓨터를 지목할 수 있음
    # 0.0.0.0을 사용: 외부서버에서도 접속가능
    # 플라스크는 테스트 프로토콜로 5000번 사용: 웹 서버가 실행중인 프로토콜 포트번포, 제품 서버에 사용되는 80번을 사용하지 않는다.