import sys
from flask import Flask, request, Response
import ujson as json	#we are using ujson instead of json for performance reasons --> import json
from bid_optimizer import BidOptimizer
import account_manager as acc

load_model = False #for const we don't load ctr prediction model
app = Flask(__name__)
opt = BidOptimizer(load_model)

@app.route('/win/<bid_id>/<bid_val>')
def win(bid_id, bid_val):
    acc.adjust_total_spend(bid_id, bid_val)
    return Response(status=200, mimetype='application/json')

@app.route('/bidders/nobid', methods=['POST'])
def nobid_bidder():
    return Response(status=204, mimetype='application/json')

@app.route('/bidders/const', methods=['POST'])
def const_bidder():
    bid_val = opt.const_bidder(json.loads(request.data))
    if not bid_val:
        return nobid_bidder()
    #if request.headers['Content-Type'] == 'application/json':	#redundant process --> removed for optimization reason
    data = {
        'bid'  : bid_val
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

@app.route('/bidders/rand', methods=['POST'])
def rand_bidder():
    data = {
        'bid'  : opt.rand_bidder()
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

@app.route('/bidders/mcpc', methods=['POST'])
def mcpc_bidder():
    data = {
        'bid'  : opt.mcpc_bidder(json.loads(request.data))#(request.json)
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

@app.route('/bidders/lin', methods=['POST'])
def lin_bidder():
    #print request.json
    data = {
        'bid'  : opt.lin_bidder(json.loads(request.data))#(request.json)	#flask seems using standard json for decoding --> for performance reason we use ujson
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)	#set debug flag to False
