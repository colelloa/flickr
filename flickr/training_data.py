#x y height width url
#this is a terrible script
def prepare_training_data(raw):
    final_list = list()
    split_newline = raw.split('\n')
    for line in split_newline:
        if not line=='':
            each_split = line.split(' ')
            each_split = [value for value in each_split if value != ''] #prevent '' from being an element in list
            assert len(each_split) == 5

            url = each_split[4]
            x=int(float(each_split[0]))
            y=int(float(each_split[1]))
            rad = int((int(each_split[2]) + int(each_split[3]))/2)

            final_list.append([url, [y, x, rad]])                   
    return final_list


RAW_TRAINING_DATA = '''255 274.5   162 157 https://farm2.staticflickr.com/1102/5117093816_a9c4c383c9.jpg
154 252 86  84  https://farm4.staticflickr.com/3521/3753864330_fc3d36755a.jpg
103.5   258 49  52  https://farm3.staticflickr.com/2643/3753861818_662a81c0c6.jpg
306 244.5   86  87  https://farm4.staticflickr.com/3489/3753869790_4956e5478c.jpg
96  354.5   60  57  https://farm4.staticflickr.com/3429/3753074355_dea84d53b2.jpg
360.5   117 147 142 https://farm4.staticflickr.com/3001/2519474886_4c4dd87d5f.jpg
105.5   390 121 114 https://farm3.staticflickr.com/2489/3753094819_3b182acf02.jpg
121 398 152 150 https://farm3.staticflickr.com/2636/3753886656_7697149ebe.jpg
131.5   385 149 144 https://farm4.staticflickr.com/3499/3753884788_b7ec790071.jpg
73.5    389.5   89  93  https://farm3.staticflickr.com/2506/3753877062_f07660f945.jpg
89  416 52  54  https://farm3.staticflickr.com/2427/3753880016_e731144ebd.jpg
227 217 158 164 https://farm3.staticflickr.com/2294/1975875218_0610e6e722.jpg
96.5    373 61  62  https://farm3.staticflickr.com/2598/3753084645_9136798d32.jpg
348.5   182.5   139 129 https://farm6.staticflickr.com/5028/5690773693_bbd9520e4f.jpg
354.5   391.5   139 137 https://farm6.staticflickr.com/5540/9656873877_c8a4b9849f.jpg
227.5   204.5   127 121 https://farm9.staticflickr.com/8432/7811952096_4178084a54.jpg
0   0   0   0   https://farm9.staticflickr.com/8738/16580900700_37478070f3.jpg
328 333.5   118 109 https://farm5.staticflickr.com/4152/5013096054_8f233bfee3.jpg
114 242 132 118 https://farm3.staticflickr.com/2601/3753093167_d9f9a8fa55.jpg
312 256 88  84  https://farm3.staticflickr.com/2659/3753867028_73931a286d.jpg
312.5   226.5   81  71  https://farm3.staticflickr.com/2032/3527881656_f0be589676.jpg
142.5   301 71  66  https://farm3.staticflickr.com/2452/3753076605_65a1fb419d.jpg
0   0   0   0   https://farm6.staticflickr.com/5213/5499702132_af85b3c4f6.jpg
371.5   317 71  64  https://farm7.staticflickr.com/6238/6269694594_1ffdb581f3.jpg
247.5   305.5   133 123 https://farm6.staticflickr.com/5490/9279832145_ab3387f586.jpg
174.5   322.5   143 131 https://farm4.staticflickr.com/3131/2618131351_3829c92635.jpg
369.5   352.5   79  73  https://farm7.staticflickr.com/6178/6269618452_e4a3411dc7.jpg
0   0   0   0   https://farm8.staticflickr.com/7205/6850895027_2403bc6999.jpg
169 419.5   86  83  https://farm2.staticflickr.com/1292/1391640704_23c231f31b.jpg
191 286 118 112 https://farm2.staticflickr.com/1051/5140569497_63602dc0a0.jpg
83.5    416.5   49  49  https://farm3.staticflickr.com/2551/3753091335_e5cb47c11f.jpg
429.5   180 135 138 https://farm4.staticflickr.com/3206/3001332120_ed81b77c94.jpg
373 218 92  86  https://farm5.staticflickr.com/4058/4692491212_87d9cdc99c.jpg
424 179 136 128 https://farm4.staticflickr.com/3206/3001332120_ed81b77c94.jpg
0   0   0   0   https://farm8.staticflickr.com/7043/6861487717_a51f8705c9.jpg
0   0   0   0   https://farm9.staticflickr.com/8243/8654383681_da0bbc2b0f.jpg
289 265 58  46  https://farm7.staticflickr.com/6129/6000443501_631dd97fa5.jpg
0   0   0   0   https://farm7.staticflickr.com/6071/6084527296_75c2c8301c.jpg
333 294 70  52  https://farm7.staticflickr.com/6060/5911123057_037043d895.jpg
0   0   0   0   https://farm8.staticflickr.com/7023/6845379305_bf03af9f36.jpg
301 207 136 132 https://farm4.staticflickr.com/3106/2459586784_843dc652df.jpg
248.5   188 163 154 https://farm3.staticflickr.com/2257/2469289672_25e70ae282.jpg
0   0   0   0   https://farm8.staticflickr.com/7023/6845379305_bf03af9f36.jpg
0   0   0   0   https://farm9.staticflickr.com/8287/7736076572_cc8b28969b.jpg
0   0   0   0   https://farm8.staticflickr.com/7174/6845379565_bb828dc7f1.jpg
0   0   0   0   https://farm1.staticflickr.com/323/18790636003_6828318059.jpg
305 205 130 128 https://farm4.staticflickr.com/3106/2459586784_843dc652df.jpg
0   0   0   0   https://farm7.staticflickr.com/6020/5952464709_197365a797.jpg
0   0   0   0   https://farm2.staticflickr.com/1321/602728336_1698ba605d.jpg
144 242 116 112 https://farm5.staticflickr.com/4048/4236808552_da55477e04.jpg
0   0   0   0   https://farm8.staticflickr.com/7333/10467602134_90cfcb304e.jpg
0   0   0   0   https://farm4.staticflickr.com/3477/3747546776_7ca1cedf14.jpg
0   0   0   0   https://farm7.staticflickr.com/6123/5952461529_f838a76e1d.jpg
0   0   0   0   https://farm7.staticflickr.com/6020/5952464709_197365a797.jpg
0   0   0   0   https://farm4.staticflickr.com/3165/2983731035_23cf655a26.jpg
0   0   0   0   https://farm1.staticflickr.com/669/22976842711_26cae62ca0.jpg
346 305.5   24  23  https://farm3.staticflickr.com/2899/14287401717_88f03f20e9.jpg
165.5   173 3   2   https://farm3.staticflickr.com/2324/2471736899_e627634f21.jpg
0   0   0   0   https://farm3.staticflickr.com/2245/2099351112_4c62f27d6c.jpg
0   0   0   0   https://farm2.staticflickr.com/1411/602790510_d5af543dce.jpg
0   0   0   0   https://farm7.staticflickr.com/6002/5953005212_79e5df582a.jpg
0   0   0   0   https://farm7.staticflickr.com/6027/5952468069_58d4f427eb.jpg
0   0   0   0   https://farm6.staticflickr.com/5226/5851698262_73bfeffdb7.jpg
0   0   0   0   https://farm3.staticflickr.com/2598/5851129275_b85a1a6bbe.jpg
0   0   0   0   https://farm7.staticflickr.com/6132/5953007594_4fa6693585.jpg
'''
prepare_training_data(RAW_TRAINING_DATA)