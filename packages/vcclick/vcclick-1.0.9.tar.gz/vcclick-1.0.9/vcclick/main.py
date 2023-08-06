import numpy as np #line:2
from copy import deepcopy #line:3
import matplotlib .pyplot as plt #line:4
import cv2 #line:5
def show (O000OOOO00000OOO0 ):#line:7
    plt .figure (figsize =(8 ,8 ))#line:8
    if np .max (O000OOOO00000OOO0 )==1 :#line:10
        plt .imshow (O000OOOO00000OOO0 ,vmin =0 ,vmax =1 )#line:11
    else :#line:12
        plt .imshow (O000OOOO00000OOO0 ,vmin =0 ,vmax =255 )#line:13
    plt .gray ()#line:14
    plt .show ()#line:15
    plt .close ()#line:16
    print ()#line:17
def resize (OO00O0000000000O0 ,O0OO0O00OO0O0O000 ):#line:19
    OOO0000OO000O0000 ,OO00O000OO0O0OO00 =OO00O0000000000O0 .shape [:2 ]#line:21
    if OOO0000OO000O0000 <OO00O000OO0O0OO00 :#line:23
        O00O0000O0O00O000 =O0OO0O00OO0O0O000 #line:24
        OO0O0OOO0O00O0OO0 =int (OOO0000OO000O0000 *O0OO0O00OO0O0O000 /OO00O000OO0O0OO00 )#line:25
        OO00O0O00OOOO000O =OO00O000OO0O0OO00 /O0OO0O00OO0O0O000 #line:26
    else :#line:27
        OO0O0OOO0O00O0OO0 =O0OO0O00OO0O0O000 #line:28
        O00O0000O0O00O000 =int (OO00O000OO0O0OO00 *O0OO0O00OO0O0O000 /OOO0000OO000O0000 )#line:29
        OO00O0O00OOOO000O =OOO0000OO000O0000 /O0OO0O00OO0O0O000 #line:30
    OO00O0000000000O0 =cv2 .resize (OO00O0000000000O0 ,(O00O0000O0O00O000 ,OO0O0OOO0O00O0OO0 ),interpolation =cv2 .INTER_CUBIC )#line:31
    print ('------------------------------------')#line:33
    print ('resizing in window size ({}, {})'.format (O00O0000O0O00O000 ,OO0O0OOO0O00O0OO0 ))#line:34
    print ('(w, h) = ({}, {})'.format (OO00O000OO0O0OO00 ,OOO0000OO000O0000 ))#line:35
    print ('(w, h) = ({}, {})'.format (O00O0000O0O00O000 ,OO0O0OOO0O00O0OO0 ))#line:36
    return OO00O0000000000O0 ,OO00O0O00OOOO000O #line:37
class pointlist ():#line:39
    def __init__ (O0OO0OOO0OOOO0O0O ):#line:40
        O0OO0OOO0OOOO0O0O .points =[]#line:41
        O0OO0OOO0OOOO0O0O .L =[]#line:42
        O0OO0OOO0OOOO0O0O .R =[]#line:43
        O0OO0OOO0OOOO0O0O .state =None #line:44
    def add (O0OOO0O000O00OOOO ,O00O0O00O00O0000O ,OO0O000O0OO0OO00O ,OOO000O0OOO0OO00O ):#line:46
        O0OOO0O000O00OOOO .points .append ([O00O0O00O00O0000O ,OO0O000O0OO0OO00O ])#line:47
        if OOO000O0OOO0OO00O =='L':#line:48
            O0OOO0O000O00OOOO .L .append ([O00O0O00O00O0000O ,OO0O000O0OO0OO00O ])#line:49
            O0OOO0O000O00OOOO .state ='L'#line:50
        if OOO000O0OOO0OO00O =='R':#line:51
            O0OOO0O000O00OOOO .R .append ([O00O0O00O00O0000O ,OO0O000O0OO0OO00O ])#line:52
            O0OOO0O000O00OOOO .state ='R'#line:53
        print ('points[{}] = ({}, {})'.format (len (O0OOO0O000O00OOOO .points )-1 ,O00O0O00O00O0000O ,OO0O000O0OO0OO00O ))#line:54
class vcclick :#line:56
    def __init__ (OO000OOOO0OOOO00O ):#line:57
        pass #line:58
    def __del__ (OO000000OO00O0OOO ):#line:59
        pass #line:60
    def get_draw (OOOOO000OOOOO00O0 ,return_size ='original'):#line:62
        if return_size =='original':#line:63
            OOOOO000OOOOO00O0 .img_draw_original =cv2 .resize (OOOOO000OOOOO00O0 .img_draw ,OOOOO000OOOOO00O0 .img_original .shape [:2 ][::-1 ],interpolation =cv2 .INTER_CUBIC )#line:64
            return OOOOO000OOOOO00O0 .img_draw_original #line:65
        else :#line:66
            return OOOOO000OOOOO00O0 .img_draw #line:67
    def get_mask (O0OO00OOO00O0O000 ,return_size ='original'):#line:69
        if O0OO00OOO00O0O000 .mode =='single':#line:70
            if return_size =='original':#line:71
                OO0OO0OO000OO0O00 =np .zeros (O0OO00OOO00O0O000 .img_original .shape ,int )#line:72
                O00000OO000OOO0O0 =np .array (O0OO00OOO00O0O000 .points .points )*O0OO00OOO00O0O000 .rate #line:73
                O00000OO000OOO0O0 =O00000OO000OOO0O0 .astype (int )#line:74
                cv2 .fillConvexPoly (OO0OO0OO000OO0O00 ,points =O00000OO000OOO0O0 ,color =(1 ,1 ,1 ))#line:75
            else :#line:76
                OO0OO0OO000OO0O00 =np .zeros (O0OO00OOO00O0O000 .img .shape ,int )#line:77
                O00000OO000OOO0O0 =np .array (O0OO00OOO00O0O000 .points .points )#line:78
                cv2 .fillConvexPoly (OO0OO0OO000OO0O00 ,points =O00000OO000OOO0O0 ,color =(1 ,1 ,1 ))#line:79
        if O0OO00OOO00O0O000 .mode =='multi':#line:80
            if return_size =='original':#line:81
                OO0OO0OO000OO0O00 =np .zeros (O0OO00OOO00O0O000 .img_original .shape ,int )#line:82
                for OO0O00000O0000O0O in O0OO00OOO00O0O000 .points_set :#line:84
                    O00000OO000OOO0O0 =np .array (OO0O00000O0000O0O )*O0OO00OOO00O0O000 .rate #line:85
                    O00000OO000OOO0O0 =O00000OO000OOO0O0 .astype (int )#line:86
                    cv2 .fillConvexPoly (OO0OO0OO000OO0O00 ,points =O00000OO000OOO0O0 ,color =(1 ,1 ,1 ))#line:87
            else :#line:88
                OO0OO0OO000OO0O00 =np .zeros (O0OO00OOO00O0O000 .img .shape ,int )#line:89
                for OO0O00000O0000O0O in O0OO00OOO00O0O000 .points_set :#line:91
                    O00000OO000OOO0O0 =np .array (OO0O00000O0000O0O )#line:92
                    cv2 .fillConvexPoly (OO0OO0OO000OO0O00 ,points =O00000OO000OOO0O0 ,color =(1 ,1 ,1 ))#line:93
        OO0OO0OO000OO0O00 =np .sum (OO0OO0OO000OO0O00 ,axis =2 )==3 #line:94
        return OO0OO0OO000OO0O00 #line:95
    def single (OOOO0O0000O0O00O0 ,OOOOO0OOO000OO0OO ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original',points_num =None ):#line:102
        OOOO0O0000O0O00O0 .img_original =np .array (OOOOO0OOO000OO0OO )#line:104
        OOOO0O0000O0O00O0 .window_size =window_size #line:105
        assert guide ==None or len (guide )==3 #line:106
        assert marker ==None or len (marker )==3 #line:107
        assert line ==None or len (line )==3 #line:108
        OOOO0O0000O0O00O0 .guide =guide [::-1 ]if guide !=None else None #line:109
        OOOO0O0000O0O00O0 .marker =marker [::-1 ]if marker !=None else None #line:110
        OOOO0O0000O0O00O0 .line =line [::-1 ]if line !=None else None #line:111
        OOOO0O0000O0O00O0 .points =pointlist ()#line:112
        OOOO0O0000O0O00O0 .points_set =[]#line:113
        OOOO0O0000O0O00O0 .points_num =points_num #line:114
        OOOO0O0000O0O00O0 .wname ='aaa'#line:115
        OOOO0O0000O0O00O0 .img ,OOOO0O0000O0O00O0 .rate =resize (OOOO0O0000O0O00O0 .img_original ,OOOO0O0000O0O00O0 .window_size )#line:118
        OOOO0O0000O0O00O0 .h ,OOOO0O0000O0O00O0 .w =OOOO0O0000O0O00O0 .img .shape [:2 ]#line:120
        OOOO0O0000O0O00O0 .img_draw =deepcopy (OOOO0O0000O0O00O0 .img )#line:121
        OOOO0O0000O0O00O0 .mode ='single'#line:124
        cv2 .namedWindow (OOOO0O0000O0O00O0 .wname )#line:125
        cv2 .startWindowThread ()#line:126
        cv2 .setMouseCallback (OOOO0O0000O0O00O0 .wname ,OOOO0O0000O0O00O0 .start )#line:127
        cv2 .imshow (OOOO0O0000O0O00O0 .wname ,OOOO0O0000O0O00O0 .img )#line:129
        cv2 .waitKey ()#line:130
        if return_size =='original':#line:133
            print ('return in original size {}'.format (OOOO0O0000O0O00O0 .img_original .shape [:2 ][::-1 ]))#line:134
            print ('------------------------------------')#line:135
            return np .array (OOOO0O0000O0O00O0 .points .points )*OOOO0O0000O0O00O0 .rate #line:136
        else :#line:137
            print ('return in window size {}'.format (OOOO0O0000O0O00O0 .img .shape [:2 ][::-1 ]))#line:138
            return np .array (OOOO0O0000O0O00O0 .points .points )#line:139
    def multi (O0OOOO0O0OOOO0000 ,O0OOOO000O00OO00O ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original',points_num =None ):#line:146
        O0OOOO0O0OOOO0000 .img_original =np .array (O0OOOO000O00OO00O )#line:148
        O0OOOO0O0OOOO0000 .window_size =window_size #line:149
        assert guide ==None or len (guide )==3 #line:150
        assert marker ==None or len (marker )==3 #line:151
        assert line ==None or len (line )==3 #line:152
        O0OOOO0O0OOOO0000 .guide =guide [::-1 ]if guide !=None else None #line:153
        O0OOOO0O0OOOO0000 .marker =marker [::-1 ]if marker !=None else None #line:154
        O0OOOO0O0OOOO0000 .line =line [::-1 ]if line !=None else None #line:155
        O0OOOO0O0OOOO0000 .points =pointlist ()#line:156
        O0OOOO0O0OOOO0000 .points_set =[]#line:157
        O0OOOO0O0OOOO0000 .points_num =points_num #line:158
        O0OOOO0O0OOOO0000 .wname ='aaa'#line:159
        O0OOOO0O0OOOO0000 .img ,O0OOOO0O0OOOO0000 .rate =resize (O0OOOO0O0OOOO0000 .img_original ,O0OOOO0O0OOOO0000 .window_size )#line:162
        O0OOOO0O0OOOO0000 .h ,O0OOOO0O0OOOO0000 .w =O0OOOO0O0OOOO0000 .img .shape [:2 ]#line:164
        O0OOOO0O0OOOO0000 .img_draw =deepcopy (O0OOOO0O0OOOO0000 .img )#line:165
        O0OOOO0O0OOOO0000 .mode ='multi'#line:168
        cv2 .namedWindow (O0OOOO0O0OOOO0000 .wname )#line:169
        cv2 .startWindowThread ()#line:170
        cv2 .setMouseCallback (O0OOOO0O0OOOO0000 .wname ,O0OOOO0O0OOOO0000 .start )#line:171
        cv2 .imshow (O0OOOO0O0OOOO0000 .wname ,O0OOOO0O0OOOO0000 .img )#line:173
        cv2 .waitKey ()#line:174
        if return_size =='original':#line:177
            print ('return in original size {}'.format (O0OOOO0O0OOOO0000 .img_original .shape [:2 ][::-1 ]))#line:178
            print ('------------------------------------')#line:179
            OOOOO0OOO000O00OO =deepcopy (O0OOOO0O0OOOO0000 .points_set )#line:180
            for O0O00O00O00O0O0O0 in range (len (OOOOO0OOO000O00OO )):#line:181
                OOOOO0OOO000O00OO [O0O00O00O00O0O0O0 ]=np .array (OOOOO0OOO000O00OO [O0O00O00O00O0O0O0 ])*O0OOOO0O0OOOO0000 .rate #line:182
            return OOOOO0OOO000O00OO #line:183
        else :#line:184
            print ('return in window size {}'.format (O0OOOO0O0OOOO0000 .img .shape [:2 ][::-1 ]))#line:185
            OOOOO0OOO000O00OO =deepcopy (O0OOOO0O0OOOO0000 .points_set )#line:186
            for O0O00O00O00O0O0O0 in range (len (OOOOO0OOO000O00OO )):#line:187
                OOOOO0OOO000O00OO [O0O00O00O00O0O0O0 ]=np .array (OOOOO0OOO000O00OO [O0O00O00O00O0O0O0 ])#line:188
            return O0OOOO0O0OOOO0000 .points_set #line:189
    def start (O000OOOOOOO0O0OOO ,O000OO00O0OO0O0O0 ,OOO0O00OOO00O00OO ,O0000O000000O0OOO ,O00O0OO000O00000O ,O0O0O0OO00O00OOO0 ):#line:192
        if O000OO00O0OO0O0O0 ==cv2 .EVENT_MBUTTONDOWN and O000OOOOOOO0O0OOO .points .state !='L':#line:194
            for OOOOO0OO00OO0O0O0 in range (1 ,10 ):cv2 .waitKey (1 )#line:195
            cv2 .destroyWindow ('aaa')#line:196
            for OOOOO0OO00OO0O0O0 in range (1 ,10 ):cv2 .waitKey (1 )#line:197
        if O000OO00O0OO0O0O0 ==cv2 .EVENT_MOUSEMOVE :#line:200
            OOO000OO0OO000O0O =deepcopy (O000OOOOOOO0O0OOO .img_draw )#line:202
            if O000OOOOOOO0O0OOO .guide !=None :#line:204
                cv2 .line (OOO000OO0OO000O0O ,(OOO0O00OOO00O00OO ,0 ),(OOO0O00OOO00O00OO ,O000OOOOOOO0O0OOO .h -1 ),O000OOOOOOO0O0OOO .guide )#line:205
                cv2 .line (OOO000OO0OO000O0O ,(0 ,O0000O000000O0OOO ),(O000OOOOOOO0O0OOO .w -1 ,O0000O000000O0OOO ),O000OOOOOOO0O0OOO .guide )#line:206
            if O000OOOOOOO0O0OOO .points .state =='L':#line:208
                if O000OOOOOOO0O0OOO .line !=None :#line:209
                    OO0O00O000O00OOO0 ,O0O00O0OO0O0O0000 =O000OOOOOOO0O0OOO .points .L [-1 ]#line:210
                    cv2 .line (OOO000OO0OO000O0O ,(OO0O00O000O00OOO0 ,O0O00O0OO0O0O0000 ),(OOO0O00OOO00O00OO ,O0000O000000O0OOO ),O000OOOOOOO0O0OOO .guide )#line:211
            cv2 .imshow (O000OOOOOOO0O0OOO .wname ,OOO000OO0OO000O0O )#line:213
        if O000OO00O0OO0O0O0 ==cv2 .EVENT_LBUTTONDOWN :#line:216
            if O000OOOOOOO0O0OOO .points .state =='L':#line:218
                cv2 .circle (O000OOOOOOO0O0OOO .img_draw ,(OOO0O00OOO00O00OO ,O0000O000000O0OOO ),4 ,O000OOOOOOO0O0OOO .marker ,1 )#line:220
                if O000OOOOOOO0O0OOO .line !=None :#line:222
                    OO0O00O000O00OOO0 ,O0O00O0OO0O0O0000 =O000OOOOOOO0O0OOO .points .L [-1 ]#line:223
                    cv2 .line (O000OOOOOOO0O0OOO .img_draw ,(OO0O00O000O00OOO0 ,O0O00O0OO0O0O0000 ),(OOO0O00OOO00O00OO ,O0000O000000O0OOO ),O000OOOOOOO0O0OOO .line )#line:224
                O000OOOOOOO0O0OOO .points .add (OOO0O00OOO00O00OO ,O0000O000000O0OOO ,'L')#line:226
                cv2 .imshow (O000OOOOOOO0O0OOO .wname ,O000OOOOOOO0O0OOO .img_draw )#line:228
                if O000OOOOOOO0O0OOO .mode =='single'and len (O000OOOOOOO0O0OOO .points .points )==O000OOOOOOO0O0OOO .points_num :#line:231
                    for OOOOO0OO00OO0O0O0 in range (1 ,10 ):cv2 .waitKey (1 )#line:232
                    cv2 .destroyWindow ('aaa')#line:233
                    for OOOOO0OO00OO0O0O0 in range (1 ,10 ):cv2 .waitKey (1 )#line:234
                if O000OOOOOOO0O0OOO .mode =='multi'and len (O000OOOOOOO0O0OOO .points .points )==O000OOOOOOO0O0OOO .points_num :#line:236
                    O000OOOOOOO0O0OOO .points_set .append (O000OOOOOOO0O0OOO .points .points )#line:237
                    O000OOOOOOO0O0OOO .points =pointlist ()#line:238
            else :#line:241
                O000OOOOOOO0O0OOO .points .add (OOO0O00OOO00O00OO ,O0000O000000O0OOO ,'L')#line:243
                cv2 .circle (O000OOOOOOO0O0OOO .img_draw ,(OOO0O00OOO00O00OO ,O0000O000000O0OOO ),4 ,O000OOOOOOO0O0OOO .marker ,1 )#line:245
                cv2 .imshow (O000OOOOOOO0O0OOO .wname ,O000OOOOOOO0O0OOO .img_draw )#line:247
        if O000OO00O0OO0O0O0 ==cv2 .EVENT_RBUTTONDOWN :#line:250
            if O000OOOOOOO0O0OOO .points .state =='L':#line:252
                cv2 .circle (O000OOOOOOO0O0OOO .img_draw ,(OOO0O00OOO00O00OO ,O0000O000000O0OOO ),4 ,O000OOOOOOO0O0OOO .marker ,1 )#line:254
                if O000OOOOOOO0O0OOO .line !=None :#line:256
                    OO0O00O000O00OOO0 ,O0O00O0OO0O0O0000 =O000OOOOOOO0O0OOO .points .L [-1 ]#line:257
                    cv2 .line (O000OOOOOOO0O0OOO .img_draw ,(OO0O00O000O00OOO0 ,O0O00O0OO0O0O0000 ),(OOO0O00OOO00O00OO ,O0000O000000O0OOO ),O000OOOOOOO0O0OOO .line )#line:258
                O000OOOOOOO0O0OOO .points .add (OOO0O00OOO00O00OO ,O0000O000000O0OOO ,'R')#line:260
                cv2 .imshow (O000OOOOOOO0O0OOO .wname ,O000OOOOOOO0O0OOO .img_draw )#line:262
                if O000OOOOOOO0O0OOO .mode =='multi':#line:265
                    O000OOOOOOO0O0OOO .points_set .append (O000OOOOOOO0O0OOO .points .points )#line:266
                    O000OOOOOOO0O0OOO .points =pointlist ()#line:267
            else :#line:270
                pass #line:271
            if O000OOOOOOO0O0OOO .mode =='single':#line:274
                for OOOOO0OO00OO0O0O0 in range (1 ,10 ):cv2 .waitKey (1 )#line:275
                cv2 .destroyWindow ('aaa')#line:276
                for OOOOO0OO00OO0O0O0 in range (1 ,10 ):cv2 .waitKey (1 )#line:277
if __name__ =='__main__':#line:280
    file_name ='yoko.JPG'#line:282
    img =cv2 .imread (file_name )#line:287
    show (img )#line:288
    myclick =vcclick ()#line:291
    points =myclick .multi (img ,points_num =4 )#line:292
    print (points )#line:293
    img_mark =myclick .get_draw ()#line:295
    show (img_mark )#line:296
    mask =myclick .get_mask ()#line:298
    show (mask )#line:299
