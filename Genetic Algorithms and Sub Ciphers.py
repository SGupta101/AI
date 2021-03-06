import sys
import math
import numpy
import random
import string

POPULATION_SIZE = 500
CLONES = 1
TOURNAMENT_SIZE = 60
TOURNAMENT_WIN = .25
CROSSOVER_POINTS = 5
MUTATION_RATE = .8
NGRAMS_TEXT = "ngrams1.tsv"
NGRAMS_TO_FREQUENCY = {}
N = 5
reached_n = False
BASE = 2
# MESSAGE = "PF HACYHTTRQ VF N PBYYRPGVBA BS SERR YRNEAVAT NPGVIVGVRF GUNG GRNPU PBZCHGRE FPVRAPR GUEBHTU RATNTVAT TNZRF NAQ CHMMYRF GUNG HFR PNEQF, FGEVAT, PENLBAF NAQ YBGF BS EHAAVAT NEBHAQ. JR BEVTVANYYL QRIRYBCRQ GUVF FB GUNG LBHAT FGHQRAGF PBHYQ QVIR URNQ-SVEFG VAGB PBZCHGRE FPVRAPR, RKCREVRAPVAT GUR XVAQF BS DHRFGVBAF NAQ PUNYYRATRF GUNG PBZCHGRE FPVRAGVFGF RKCREVRAPR, OHG JVGUBHG UNIVAT GB YRNEA CEBTENZZVAT SVEFG.  GUR PBYYRPGVBA JNF BEVTVANYYL VAGRAQRQ NF N ERFBHEPR SBE BHGERNPU NAQ RKGRAFVBA, OHG JVGU GUR NQBCGVBA BS PBZCHGVAT NAQ PBZCHGNGVBANY GUVAXVAT VAGB ZNAL PYNFFEBBZF NEBHAQ GUR JBEYQ, VG VF ABJ JVQRYL HFRQ SBE GRNPUVAT. GUR ZNGREVNY UNF ORRA HFRQ VA ZNAL PBAGRKGF BHGFVQR GUR PYNFFEBBZ NF JRYY, VAPYHQVAT FPVRAPR FUBJF, GNYXF SBE FRAVBE PVGVMRAF, NAQ FCRPVNY RIRAGF.  GUNAXF GB TRAREBHF FCBAFBEFUVCF JR UNIR ORRA NOYR GB PERNGR NFFBPVNGRQ ERFBHEPRF FHPU NF GUR IVQRBF, JUVPU NER VAGRAQRQ GB URYC GRNPUREF FRR UBJ GUR NPGVIVGVRF JBEX (CYRNFR QBA'G FUBJ GURZ GB LBHE PYNFFRF – YRG GURZ RKCREVRAPR GUR NPGVIVGVRF GURZFRYIRF!). NYY BS GUR NPGVIVGVRF GUNG JR CEBIVQR NER BCRA FBHEPR – GURL NER ERYRNFRQ HAQRE N PERNGVIR PBZZBAF NGGEVOHGVBA-FUNERNYVXR YVPRAPR, FB LBH PNA PBCL, FUNER NAQ ZBQVSL GUR ZNGREVNY.  SBE NA RKCYNANGVBA BA GUR PBAARPGVBAF ORGJRRA PF HACYHTTRQ NAQ PBZCHGNGVBANY GUVAXVAT FXVYYF, FRR BHE PBZCHGNGVBANY GUVAXVAT NAQ PF HACYHTTRQ CNTR.  GB IVRJ GUR GRNZ BS PBAGEVOHGBEF JUB JBEX BA GUVF CEBWRPG, FRR BHE CRBCYR CNTR.  SBE QRGNVYF BA UBJ GB PBAGNPG HF, FRR BHE PBAGNPG HF CNTR.  SBE ZBER VASBEZNGVBA NOBHG GUR CEVAPVCYRF ORUVAQ PF HACYHTTRQ, FRR BHE CEVAPVCYRF CNTR."
# MESSAGE = "LTQCXT LRJJ HJRDECD, EZT CDJP SXTFRYTDE EC ZNKT LTTD RASTNHZTY VNF NDYXTV WCZDFCD. ZT VNF NHUBREETY LP N FRDGJT KCET VZTD N LXNKT FTDNECX QXCA ONDFNF XTQBFTY EC PRTJY QXCA SXTFFBXT EC HCDKRHE EZT SXTFRYTDE. ZNY WCZDFCD LTTD HCDKRHETY, EZT FSTNOTX CQ EZT ZCBFT VCBJY ZNKT LTHCAT SXTFRYTDE FRDHT WCZDFCD ZNY DC KRHTSXTFRYTDE. RDHXTYRLJP, RE VNF EZRF FNAT FSTNOTX VZC JTY EZT RASTNHZATDE RD EZT ZCBFT CQ XTSXTFTDENERKTF. EZBF, ZNY EZT FTDNET HCDKRHETY EZT SXTFRYTDE, EZRF VCBJY ZNKT NACBDETY EC N SCJRERHNJ HCBS."
# MESSAGE = "ZRTGO Y JPEYPGZA, RP'J IKPGO HIJJRMWG PI RSHEITG PUG JPEYPGZA MA SYDROZ EYOBIS XUYOZGJ, PGJPROZ PUG EGJLWP IK PUIJG XUYOZGJ, YOB DGGHROZ IOWA PUG MGPPGE ILPXISGJ.  PURJ RJ XYWWGB URWW XWRSMROZ.  PURJ RJ EGWYPRTGWA JRSHWG PI XIBG, MLP BIGJO'P CIED RO GTGEA JRPLYPRIO - RP XYO IKPGO ZGP XYLZUP RO Y WIXYW SYFRSLS, Y JPEYPGZA PUYP RJ OIP RBGYW MLP KEIS CURXU YOA JROZWG XUYOZG RJ OIP YO RSHEITGSGOP IO RPJ ICO. ZGOGPRX YWZIERPUSJ YEG Y HICGEKLW PIIW KIE RSHEITROZ IO PUG RBGY IK URWW XWRSMROZ PI IHPRSRVG Y JIWLPRIO RO JRPLYPRIOJ CUGEG YWW IK PUG KIWWICROZ YEG PELG: Y JPEYPGZA XYO MG HEGXRJGWA QLYOPRKRGB MA Y JHGXRKRX JGP IK TYERYMWGJ ZRTGO XGEPYRO OLSGERX TYWLGJ. PUG ILPXISG IK PUG JPEYPGZA XYO YWJI MG HEGXRJGWA QLYOPRKRGB. PUGEG YEG ROPGEYXPRIOJ MGPCGGO PUG TYERYMWGJ PUYP SYDG JRSHWG URWW XWRSMROZ ROGKKRXRGOP IE LOWRDGWA PI JLXXGGB."
# MESSAGE = "CWQ KHTTQKC TFAZJAB HS FGG HS CWQ ECFT YFTE PHRJQE TQGQFEQM EH SFT JE CWQ QPXJTQ ECTJZQE VFKZ, F AQY WHXQ, CWQ GFEC OQMJ, TQCLTA HS CWQ OQMJ, THBLQ HAQ, EHGH, TQRQABQ HS CWQ EJCW, CWQ SHTKQ FYFZQAE, TJEQ HS CWQ EZNYFGZQT, CWQ XWFACHP PQAFKQ, FCCFKZ HS CWQ KGHAQE.  CWQ KHTTQKC TFAZJAB HS CWQ CWTQQ JAMJFAF OHAQE PHRJQE JE CWQ GFEC KTLEFMQ, TFJMQTE HS CWQ GHEC FTZ, CQPXGQ HS MHHP.  CWQTQ JE AH SHLTCW JAMJFAF OHAQE PHRJQ, FAM FANHAQ YWH CQGGE NHL HCWQTYJEQ JE F GJFT.  OLEC CQGG CWQP CH CLTA FTHLAM FAM YFGZ FYFN VQSHTQ CWQN KFA VGQEE NHL YJCW FAN HCWQT JAKHTTQKC HXJAJHAE.  FANYFN, EH EFNQCW PN STJQAM VJGG, YWH WFXXQAQM CH VQ HAGJAQ YWJGQ J YFE PFZJAB CWJE FEEJBAPQAC, YWQA J FEZQM WJP 'YWFC YHLGM VQ F BHHM EQKTQC PQEEFBQ SHT PN ECLMQACE CH MQKHMQ?'  XGQFEQ CFZQ LX FAN KHPXGFJACE YJCW WJP."
# MESSAGE = "XMTP CGPQR BWEKNJB GQ OTGRB EL BEQX BWEKNJB, G RFGLI.  GR GQ BEQX ABSETQB RFGQ QBLRBLSB TQBQ EJJ RBL KMQR SMKKML VMPYQ GL BLDJGQF:  'G FEUB RM AB E DMMY QRTYBLR GL RFER SJEQQ GL RFB PMMK MC RFER RBESFBP.'"
# MESSAGE = "XTV B CHDQCL BHF GCVIVDGDHWPN ABVF ZABPPLHWL, ZTHGDFLV MBJDHW B PTHW BHF XCPPN VLBFBYPL GLVDLG TX UTVFG HLRLV CGDHW B GDHWPL LEBMIPL TX TCV ULPP-PTRLF LHWPDGA WPNIA UADZA TZZCVG GLZTHF IPBZL DH TRLVBPP XVLQCLHZN.  DX D BM WLHCDHL, D UDPP GBN MBHN, MBHN GLZTHFG ABRL IBGGLF UADPL D ABRL YLLH ALVL ITHFLVDHW MBJDHW GCZA B UTVJ.  FDGZTRLVDHW NTC ZVBZJLF MN YVBDHZADPF, ALVL, DH B GMBPPLV HCMYLV TX GLZTHFG UTCPF WDRL ML HT GCVIVDGL."
# MESSAGE = "NU XTZEIMYTNEVZ INUHU YM, ZML SPYVI NXILNFFZ XNFF IVPU N API VNTD.  NU PI ILTWU MLI, P XNW YM N FMWY JNZ JPIVMLI LUPWY NWZ MC IVNI YFZEV IVNI ITNDPIPMWNFFZ CMFFMJU 'D' NI NFF.  PUW'I IVNI ULTETPUPWY?  P CMLWD IVPU ULTETPUPWY, NWZJNZ!  NW NLIVMT JVM NFUM CMLWD IVPU ULTETPUPWY, FMWY NYM, NXILNFFZ FMUI SNWZ SMWIVU JTPIPWY N AMMH - N CLFF CPXIPMWNF UIMTZ - JPIVMLI IVNI YFZEV NI NFF.  NSNRPWY, TPYVI?"
# MESSAGE = "RHNJJCBXVCXJYQJNEJNDYDCELTHNBFTVTHNJJREFCLBEECANOTREFDNEBXTHJTNXTXECPCBAPZNSSPXTNYTXFVZCNXTSXRKRJTGTYECJRKTRDFSNHTRANGRDTNKNFEFZTTECQSNSTXCDVZRHZFEXNRGZEJRDTFEXRNDGJTFFUBNXTFSTDENGCDFZTINGCDFNDYCEZTXQRGBXTFRDFETNYCQXTANRDRDGQRITYRDEZTRXSJNHTFACKTQXTTJPNLCBECDCXRDEZTFBXQNHTLBEVREZCBEEZTSCVTXCQXRFRDGNLCKTCXFRDORDGLTJCVREKTXPABHZJROTFZNYCVFCDJPZNXYVREZJBARDCBFTYGTFNDYPCBVRJJEZTDZNKTNSXTEEPHCXXTHEDCERCDCQAPHCBDEXPNDYHCBDEXPATDNJNFNQTVPTNXFNGCRFZCBJYZNKTFNRYAPBDRKTXFTLBEDCVAPARDYZNFLTTDCSTDTYECZRGZTXKRTVFCQEZRDGF"
# MESSAGE = "W CTZV VYQXDVD MCWJ IVJJTHV, TYD VYQXDVD WM BVAA, FXK WM QXYMTWYJ MCV JVQKVM XF MCV PYWZVKJV!  YX KVTAAS, WM DXVJ!  SXP DXY'M NVAWVZV IV?  BCS BXPAD SXP YXM NVAWVZV MCTM MCWJ RVKFVQMAS QKXIPAVYM JVQKVM MVGM QXYMTWYJ MCV NV TAA, VYD TAA, HKTYDVJM JVQKVM XF TAA MCV QXJIXJ?  YXB W FVVA DWJKVJRVQMVD!  CTZV SXP DWJQXZVKVD SXPK XBY NVMMVK PAMWITMV MKPMC XF VZVKSMCWYH?  W DWDY'M MCWYL JX.  JX BCS TKV SXP HVMMWYH TAA PRRWMS TM IV?  CXYVJMAS.  YX XYV CTJ TYS ITYYVKJ MCVJV DTSJ.  ...BCTM'J MCTM?  SXP BTYM IV MX MVAA SXP MCV JVQKVM?  YXM TFMVK MCWJ LWYD XF DWJKVJRVQM!  HXXDYVJJ HKTQWXPJ IV.  NTQL BCVY W BTJ T SXPMC W BTJ YXM JX QTAAXPJ.  BCVY JXIVXYV BVAA KVJRVQMVD TYD WIRXKMTYM MXAD IV MCTM MCVS CTD JXIVMCWYH BXKMC MVAAWYH IV, W OPJM AWJMVYVD!  W DWDY'M DXPNM MCVI!  JX KPDV, CXYVJMAS.  OPJM PYTQQVRMTNAV."
# MESSAGE = "CIJUQCIZQFIZALSBPUFCRLIPBFIEIHYLXQIHYLOLILEIBFQXBZJSXDJXXDLSOLILELIPLNXASUBICJAXDJUMSBFYLISCFNDXDLSOLILXDLAJZXELBEALSBFQLKELNXXBRLHUYBAYLQHUJUSXDHUWZXIJUWLBICSZXLIHBFZRLNJFZLXDLSVFZXQHQUXDBAQOHXDZFNDUBUZLUZL"
# MESSAGE = "ZFNNANWJWYBZLKEHBZTNSKDDGJWYLWSBFNSSJWYFNKBGLKOCNKSJEBDWZFNGKLJKJNQFJPFJBXHBZTNRDKNZFNPDEJWYDRPDEGCNZNWJYFZZFLZTCNBBNBZFNNLKZFSLKONWBLCCKJANKBPHGBZFNGNLOBLWSRDCSBZFNRJWLCBFDKNJWLWSWDTDSUWDTDSUOWDQBQFLZBYDJWYZDFLGGNWZDLWUTDSUTNBJSNBZFNRDKCDKWKLYBDRYKDQJWYDCSJZFJWODRSNLWEDKJLKZUJNANWZFJWODRDCSSNLWEDKJLKZUZFNRLZFNKQNWNANKRDHWSJZFJWODRSNLWEDKJLKZU"
# MESSAGE = "FBYSNRBIYVNIJRJZSRSRJZNQCQNIJXCGTNEBSJNYKCUXCGTNONNIRNBUMZSIVSIJZNYBUAXCGURENBJRCBASIVJZUCGVZJZNKFCCUBIYOGUSNYSIXCGUOCINRJZNUNRBIBMZNJZBJXCGMBIJSVICUNJBASIVXCGUOUNBJZRJNBFSIVXCGUQSIYBIYBFFJZBJEBRUNBFSRFNKJONZSIYYCIJKSVZJSJSJRMCQSIVKCUXCGUGIISIVBJXCGSJRCIFXJZSRQCQNIJYCIJMBUNEZBJMCQNRBKJNUXCGUKNTNUYUNBQMBIJXCGRNNSJVNJJSIVMFCRNUPGRJRGUUNIYNUMBGRNXCGKNNFJZNKNNFSIVJBASIVCTNUSJRKSUNSJRKUNNYCQSJRKFCCYSIVCLNISJRJZNLUNBMZNUSIJZNLGFLSJBIYXCGUOFSIYYNTCJSCIJZNUNRRCQNJZSIVOUNBASIVBJJZNOUSMACKNTNUXEBFFSJRZCFYSIVBFFJZBJXCGAICERCJNFFQNYCXCGEBIIBVCEZNUNSJRMCTNUNYSIBFFJZNMCFCUNYFSVZJREZNUNJZNUGIBEBXRBUNUGIISIVJZNISVZJSQLCRRSOFNMCQNRJUGNSJRJBASIVCTNUXCGCZJZSRSRJZNVUNBJNRJRZCEENFSVZJSJGLENECIJMCQNYCEIBIYJZNRGIMBIJRJCLGRICEEBJMZSIVSJMCQNJUGNSJRJBASIVCTNUXCGCZJZSRSRJZNVUNBJNRJRZCE"
MESSAGE = sys.argv[1]
MESSAGES = MESSAGE.split()
MESSAGE_LIST = []
ALPHABET = list(string.ascii_uppercase)
INDEXES = list(range(26))

for CURRENT_MESSAGE in MESSAGES:  # removes white space and words that are too small
    if len(CURRENT_MESSAGE) >= N and CURRENT_MESSAGE.isalpha():
        MESSAGE_LIST.append(CURRENT_MESSAGE)

with open(NGRAMS_TEXT) as f:
    for line in f:
        if line[0] == str(N + 1):  # only for 1 digit N's
            break
        if reached_n:
            split_line = line.split()
            my_n_gram = split_line[0]
            my_frequency = split_line[1]
            NGRAMS_TO_FREQUENCY[my_n_gram] = math.log(int(my_frequency), BASE)
        if line[0] == str(N):
            reached_n = True


def change_string(words, letters_key):
    alphabet_key = {}
    for i, letter in enumerate(letters_key):
        alphabet_key[ALPHABET[i]] = letter
    new_words = []
    for word in words:
        new_word = ""
        for character in word:
            if character in alphabet_key.keys():
                new_word += alphabet_key[character]
            else:
                new_word += character
        new_words.append(new_word)
    return new_words


def population():
    return set(["".join(numpy.random.permutation(ALPHABET)) for i in range(POPULATION_SIZE)])


def fitness_function(keys):
    key_to_frequency = []
    for key in keys:
        # print("key:", key)
        new_words = change_string(MESSAGE_LIST, key)
        # print("words:", new_words)
        total_frequency = 0
        for word in new_words:
            # print(word)
            last_char_index = len(word) - N
            n_grams = [word[char_index:char_index + N] for char_index in range(last_char_index + 1)]
            # print(n_grams)
            for n_gram in n_grams:
                if n_gram in NGRAMS_TO_FREQUENCY:
                    # print(n_gram, NGRAMS_TO_FREQUENCY[n_gram])
                    total_frequency += NGRAMS_TO_FREQUENCY[n_gram]
        key_to_frequency.append((key, total_frequency))
        # print("total:", total_frequency)
    return key_to_frequency


def selection_method(keys):
    total_tournaments = random.sample(keys, (TOURNAMENT_SIZE * 2))
    tournament_one = random.sample(total_tournaments, TOURNAMENT_SIZE)
    tournament_two = []
    for tournament in total_tournaments:
        if tournament not in tournament_one:
            tournament_two.append(tournament)
    sorted_tournament_one = sorted(tournament_one, key=lambda this_tournament: this_tournament[1], reverse=True)
    sorted_tournament_two = sorted(tournament_two, key=lambda this_tournament: this_tournament[1], reverse=True)
    tournament_winner_one = sorted_tournament_one[0]
    for tournament in sorted_tournament_one:
        if random.random() < TOURNAMENT_WIN:
            tournament_winner_one = tournament
            break
    tournament_winner_two = sorted_tournament_two[0]
    for tournament in sorted_tournament_two:
        if random.random() < TOURNAMENT_WIN:
            tournament_winner_two = tournament
            break
    return tournament_winner_one, tournament_winner_two


def breeding_process(parent_one, parent_two):
    child = []
    parent_one_key = parent_one[0]
    for letter in parent_one_key:
        child.append("")
    parent_one_locations = random.sample(INDEXES, CROSSOVER_POINTS)
    parent_one_letters = []
    for location in parent_one_locations:
        parent_one_letter = parent_one_key[location]
        child[location] = parent_one_letter
        parent_one_letters.append(parent_one_letter)
    parent_two_key = parent_two[0]
    parent_two_letters = []
    for letter in parent_two_key:
        if letter not in parent_one_letters:
            parent_two_letters.append(letter)
    index = 0
    for i in range(len(child)):
        if child[i] == "":
            child[i] = parent_two_letters[index]
            index += 1
    return child


def mutation(child):
    if random.random() < MUTATION_RATE:
        random_indexes = random.sample(INDEXES, 2)
        index_one = random_indexes[0]
        index_two = random_indexes[1]
        letter_one = child[index_one]
        child[index_one] = child[index_two]
        child[index_two] = letter_one
    return child


POPULATION = population()
generation = 0
KEY_TO_FREQUENCY = fitness_function(POPULATION)
SORTED_KEY_TO_FREQUENCY = sorted(KEY_TO_FREQUENCY, key=lambda this_key_to_frequency: this_key_to_frequency[1],
                                     reverse=True)
while True:
    POPULATION = set()
    for k in range(CLONES):
        POPULATION.add(SORTED_KEY_TO_FREQUENCY[k][0])
    while len(POPULATION) <= POPULATION_SIZE:
        TOURNAMENT_ONE, TOURNAMENT_TWO = selection_method(KEY_TO_FREQUENCY)
        CHILD = breeding_process(TOURNAMENT_ONE, TOURNAMENT_TWO)
        MUTATED_CHILD = mutation(CHILD)
        FINAL_CHILD = "".join(MUTATED_CHILD)
        POPULATION.add(FINAL_CHILD)
    KEY_TO_FREQUENCY = fitness_function(POPULATION)
    SORTED_KEY_TO_FREQUENCY = sorted(KEY_TO_FREQUENCY, key=lambda this_key_to_frequency: this_key_to_frequency[1],
                                     reverse=True)
    BEST_KEY = SORTED_KEY_TO_FREQUENCY[0][0]
    BEST_MESSAGE_LIST = change_string(MESSAGES, BEST_KEY)
    BEST_MESSAGE = " ".join(BEST_MESSAGE_LIST)
    print("generation:", generation)
    print(BEST_MESSAGE)
    generation += 1
