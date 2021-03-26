from rest_framework.throttling import SimpleRateThrottle


class VisitThrottle(SimpleRateThrottle):
    # 转换频率每分钟5次，转换频率 = num/duration，其中duration可以是s/m/h/d
    rate = '5/m'
    score = 'visitor'

    # 返回一个唯一标识用以区分不同的用户
    def get_cache_key(self, request, view):
        return self.get_ident(request)  # 返回用户ip
