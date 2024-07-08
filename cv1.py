import redis
r=redis.Redis(host='localhost',port=6379,db=0)

s="pt3"
r.zadd(s,{"alfred":888,"TommyM01n":154,"TommyM02n":13,"TommyM03n":500,"TommyM04n":982,"TommyM05n":52,"TommyM06n":875,"TommyM07n":999,"TommyM08n":100,"TommyM09n":54,"TommyM10n":154})

print("nejnizsi score: "+str(r.zrangebyscore(s,0,999,withscores=True,start=0,num=1)))
print("pocet pod 100: "+str(r.zcount(s,0,100)))
print("lidi nad 850: "+str(r.zrevrangebyscore(s,999,850)))
print("alfred rank1: "+str(r.zrank(s,"alfred")))
r.zincrby(s,12,"alfred")
print("alfred rank2: "+str(r.zrank(s,"alfred")))
