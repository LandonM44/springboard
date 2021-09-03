from TikTokApi import TikTokApi

#verifyFp = "verify_kt0pmso9_Zck12MgR_ZFxK_4ID4_AmMO_Vy32IxABKKpZ"
api = TikTokApi.get_instance()
#api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
results = 10
#tiktoks = api.trending()
trending = api.by_trending(count=results, custom_verfiyFp="verify_kt0pmso9_Zck12MgR_ZFxK_4ID4_AmMO_Vy32IxABKKpZ")
#class test:
# def get_trends():
for tiktok in trending:
    print(tiktok["id"])

#print(len(trending))