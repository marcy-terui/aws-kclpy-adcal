#!env python
from amazon_kclpy import kcl
import sys, time, json, base64
import socket

def collect_metric(name, value, timestamp):
    sock = socket.socket()
    sock.connect( ("192.168.11.33", 2003) )
    sock.send("%s %d %d\n" % (name, value, timestamp))
    sock.close()

class RecordProcessor(kcl.RecordProcessorBase):

    def __init__(self):
        self.SLEEP_SECONDS = 5
        self.CHECKPOINT_RETRIES = 5
        self.CHECKPOINT_FREQ_SECONDS = 60

    def initialize(self, shard_id):
        self.largest_seq = None
        self.last_checkpoint_time = time.time()

    def checkpoint(self, checkpointer, sequence_number=None):
        for n in range(0, self.CHECKPOINT_RETRIES):
            try:
                checkpointer.checkpoint(sequence_number)
                return
            except kcl.CheckpointError as e:
                sys.stderr.write('Check point Error!! {e}.\n'.format(e=e))

            time.sleep(self.SLEEP_SECONDS)

    def process_record(self, data, partition_key, sequence_number):
        for word in ['aws','azure','gcp','softlayer']:
            if word in data:
                # date_time = time.strptime(data.created_at, "%Y-%m-%d %H:%M:%S UTC")
                # unix_time = int(time.mktime(date_time))
                collect_metric("cloud." + word, 1, time.time())
                print word

    def process_records(self, records, checkpointer):
        try:
            for record in records:
                data = base64.b64decode(record.get('data'))
                seq = record.get('sequenceNumber')
                seq = int(seq)
                key = record.get('partitionKey')
                self.process_record(data, key, seq)
                if self.largest_seq == None or seq > self.largest_seq:
                    self.largest_seq = seq
            if time.time() - self.last_checkpoint_time > self.CHECKPOINT_FREQ_SECONDS:
                self.checkpoint(checkpointer, str(self.largest_seq))
                self.last_checkpoint_time = time.time()
        except Exception as e:
            sys.stderr.write("Process Error!! {e}\n".format(e=e))

    def shutdown(self, checkpointer, reason):
        try:
            if reason == 'TERMINATE':
                self.checkpoint(checkpointer, None)
        except:
            pass

if __name__ == "__main__":
    kclprocess = kcl.KCLProcess(RecordProcessor())
    kclprocess.run()
