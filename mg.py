﻿#此工具实时获取咪咕视频的直播地址
#存至./lives/migu.txt 可以直接用TVBox APP配置
#http://127.0.0.1:9978/file/TVBoxx/MeowTV/TVBoxx/lives/migu.txt (wifi:9979)
#http://127.0.0.1:9978/file/[等于手机的/sfcard]
#/storage/emulated/0/
#此工具的保存路径/TVBoxx/MeowTV/TVBoxx/自己随便修改
#有时效性:大概4小时或更长，具体的自行测试
#不卡不卡不卡，重要的事说三遍
 
 
##关于咪咕视频的m3u8再次解析##
#https://blog.csdn.net/chouzhou9701/article/details/119260799
import requests,json,time,random
from urllib import parse
from pprint import pprint
#全部频道:https://m.miguvideo.com/m/home/f08583e602f846a5b870f3de3b673326?plt=sub&channelId=10010001005
def get_topVomsID():
    #央视的vomsID:
    url='https://program-sc.miguvideo.com/live/v2/tv-data/a5f78af9d160418eb679a6dd0429c920'
    res=requests.get(url,headers=headers)
    res_js=json.loads(res.text)['body']
    livelist=res_js['liveList']
    #all:['热门', '体育', '央视', '卫视', '地方', '影视', '新闻', '教育', ' 熊猫', '娱乐', '少儿', '纪实', '印象天下', '电台']
    mychannels=['热门',  '体育', '央视', '卫视', '影视']
    #自选频道
    #print(livelist)
    #nowVomsId=res_js['nowVomsId']
    top_names,vomsIDs=[],[]
    for list in livelist:
        top_name,vomsID=list['name'],list['vomsID']
        if top_name in mychannels:
            top_names.append(top_name)
            vomsIDs.append(vomsID)
    print(f'自选频道 :{top_names}')
    return top_names,vomsIDs
     
def get_tv_id(id):
    #CCTV节目列表now|next,图标,pID,name
    #央视:
    url=f'https://program-sc.miguvideo.com/live/v2/tv-data/{id}'
    #print(url)
    res=requests.get(url,headers=headers)
    res_js=json.loads(res.text)['body']     
    datalist=res_js['dataList']
    names,pIDs=[],[]
    for data in datalist:
        name=data['name']
        pID=data['pID']
        names.append(name)
        pIDs.append(pID)
        nw=data.get('now','')
        if nw!='':
            now=nw['startTime']+'-'+nw['endTime']+' '+nw['playName']
            if 'next' in data:
                nt=data['next']
                next=nt['startTime']+'-'+nt['endTime']+' '+nt['playName']
                print(name,pID,now,next)
            else:print(name,pID,now)
    return names,pIDs
     
def get_play_url(pIDs):
    #print(pIDs)
    h5_urls=[]
    for id in pIDs:
        #print(id)
        #rateType=3高清
        #print(id)#直播"pID":"608807420"
        url=f'https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl?contId={id}&rateType=3&startPlay=true'  
        #url='http://webapi.miguvideo.com/gateway/playurl/v2/play/playurlh5?contId=635491149&rateType=3&startPlay=true'
        #url='https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl?contId=635491149&rateType=3&startPlay=true'
        #'http://webapi.miguvideo.com/gateway/playurl/v2/play/playurlh5?contId=631780532&rateType=3&clientId=5e31849abe9be8ad087ca5fbd67b0e14&startPlay=true&xh265=false&channelId=0131_10010001005'
        #time.sleep(1)
        res=requests.get(url,headers=headers)
        play_jsons=json.loads(res.text)##仅一个源
        message=play_jsons["message"]
        if message=="SUCCESS":
            #pprint(play_jsons)
            h5_url=play_jsons['body']['urlInfo']['url']
            #TypeError: 'NoneType' 版权限制访问#cctv1608807420
            h5_urls.append(h5_url)
        else:
            print(f'ID:{id} ,版权限制，无法观看')
            h5_urls.append('error')         
    return h5_urls
 
def ddCalcu(url):
    #play_url再次解析getm3u8地址
    new_url = parse.urlparse(url)
    #print(new_url)
    para = dict(parse.parse_qsl(new_url.query))
    #print(para)
    userid = para.get("userid","")
    timestamp = para.get("timestamp","")
    ProgramID = para.get("ProgramID","")
    Channel_ID = para.get("Channel_ID","")
    puData = para.get("puData","")
    t = userid if userid else "eeeeeeeee"
    r = timestamp if timestamp else "tttttttttttttt"
    n = ProgramID if ProgramID else "ccccccccc"
    a = Channel_ID if Channel_ID else "nnnnnnnnnnnnnnnn"
    o = puData if puData else ""
    if not o:
        return url
    s = list("2624")
    u = list(t)[int(s[0])] or "e"
    l = list(r)[int(s[1])] or "t"
    c = list(n)[int(s[2])] or "c"
    f = list(a)[len(a)-int(s[3])] or "n"
    d = list(o)
    h = []
    p = 0
    #print(p*2 < len(d))
    while p*2 < len(d):
        h.append(d[len(d)-p-1])
        if p < len(d) - p -1:
            h.append(o[p])
        if p == 1:
            h.append(u)
        if p == 2:
            h.append(l)
        if p == 3:
            h.append(c)
        if p == 4:
            h.append(f)
        p += 1
    v = "".join(h)
    return url + "&ddCalcu=" + v
 
def api(new_url):
    #第三次解析
    headers={
    'Host':'h5live.gslb.cmvideo.cn',
    'Connection': 'keep-alive',
    'Accept': 'text/plain, */*; q=0.01',
    'X-Requested-With': 'mark.via',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Origin':'http://m.miguvideo.com',
    'Referer':'http://m.miguvideo.com/',
    'User-Agent':'Mozilla/5.0 (Linux; Android 10; SP300 Build/CMDCSP300;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.105 Mobile Safari/537.36'}
    #param={'crossdomain':'www'}
    time.sleep(1)
    #104:网路连接异常try
    #requests.exceptions.ConnectionError:
    try:
        res=requests.get(new_url,headers=headers,timeout=10)
        #print(res.status_code)
        m3u8=str(res.text)
        return m3u8
    except requests.exceptions.ConnectionError as e:
        print('&#10008;网络连接异常: ', e)
        return False
    except requests.exceptions.Timeout as e:
        print('&#10008;连接超时: ',e)
    except requests.exceptions.RequestException as e:
        print('&#10008;请求异常: ', e)
    except requests.exceptions.HTTPError as e:
        print(f'&#10008;HTTP错误, 状态码: {e.response.status_code}, {e}')
    except ValueError as e:
        print('&#10008;响应解析异常: ', e)
     
def run():
    top_vmos=get_topVomsID()
    top_names,vomsIDs=top_vmos[0],top_vmos[1]
     
    ftime = time.strftime("%Y%m%d %H:%M", time.localtime())
    s='&#127880;&#129419;&#129436;&#127808;&#128139;&#127908;&#127895;&#127894;\
&#127941;&#10024;&#127883;&#127795;&#127811;&#127793;&#127807;&#9752;&#128165;\
&#129351;&#129352;&#129353;&#127801;&#127989;&#65039;&#127810;&#127802;&#127885;&#127796;'
     
    f=open('migu.txt','w+')
    f.write(f'咪咕直播源,#genre#\n')
    f.write(f'by caliph21_{ftime}更新 ,https://15799848.s21v.faiusr.com/58/ABUIABA6GAAgr-2n9AUoqsakNg.mp4\n')
    f.write('串烧,https://vd4.bdstatic.com/mda-mkn4iq79ihtufbc1/sc/cae_h264/1637639849265611965/mda-mkn4iq79ihtufbc1.mp4\n\n')
    f.close()
    for i in range(len(vomsIDs)):
        pic=random.choice(s)
        top_name=top_names[i]
        print('\n',top_name,f'{i+1}/{len(vomsIDs)}')
        #time.sleep(1)
        tv_id=get_tv_id(vomsIDs[i])
        print('\n')
        #time.sleep(1)
        h5_urls=get_play_url(tv_id[1])
 
        f=open('migu.txt','a+')
        f.write(f'{pic}｜{top_name},#genre#\n\n')
        f.close()
 
        for name,url in zip(tv_id[0],h5_urls):
            #print(url)
            if url!='error':
                new_url=ddCalcu(url)
                #print(new_url)
                #time.sleep(1)
                m3u8=api(new_url+'&crossdomain=www')
                #print(url==new_url)
                if m3u8!=False:
                    #剔除104网路连接异常
                    print(f'正在更新源: {name} ……')
                    #print(m3u8)
                    with open('lives/migu.txt','a+') as f:
                        f.write(name+','+str(m3u8)+'\n')
                        f.close()
         
     
 
if __name__ == '__main__':
    #names,pIDs=[],[]
    headers={'User-Agent':'Mozilla/5.0 (Linux; Android 10; SP300 Build/CMDCSP300;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4515.105 Mobile Safari/537.36'}
    run()
    #url = "https://h5live.gslb.cmvideo.cn/migu/kailu/20200324/cctv4meihd/50/index.m3u8?msisdn=20231224165648c5b9040c723843188ccd7b0e30f81b36&mdspid=&spid=699004&netType=0&sid=2200179344&pid=2028597139×tamp=20231224165648&Channel_ID=0116_25000000-99000-100300010010001&ProgramID=608807416&ParentNodeID=-99&assertID=2200179344&client_ip=240e:478:4840:1642:17a3:aca9:695:be83&SecurityKey=20231224165648&promotionId=&mvid=2200179344&mcid=500020&playurlVersion=WX-A1-6.12.1.1-RELEASE&userid=&jmhm=&videocodec=h264&bean=mgsph5&puData=8c5826a81b06fdc46a46a9128be66cd0"
    #url='https://h5live.gslb.cmvideo.cn/wd_r2/cctv/cctv1hd/600/index.m3u8?msisdn=202312241405015bc0ae24f1bb42dc9e16ff0f7ac931f9&mdspid=&spid=699004&netType=0&sid=2201057821&pid=2028597139×tamp=20231224140501&Channel_ID=0116_25000000-99000-100300010010001&ProgramID=608807420&ParentNodeID=-99&assertID=2201057821&client_ip=240e:478:4840:1642:17a3:aca9:695:be83&SecurityKey=20231224140501&promotionId=&mvid=2201057821&mcid=500020&playurlVersion=WX-A1-6.12.1.1-RELEASE&userid=&jmhm=&videocodec=h264&bean=mgsph5&puData=3f841e2a0b365c2914ee68cd75073bdb'
    #new_url = ddCalcu(url)
    #print(new_url)
    #from transformers import CLIPModel
    #model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14", from_tf=True)
