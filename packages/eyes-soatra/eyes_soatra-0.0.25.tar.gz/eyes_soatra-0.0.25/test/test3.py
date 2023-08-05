#!python3
from eyes_soatra import eyes
import requests
import json
from lxml.html.clean import Cleaner
from lxml import html
from lxml import etree
import re
from translate import Translator
import pandas

# r = requests.get('http://127.0.0.1:5500/test/test3.html')
# h = html.fromstring(r.content)
# etree.strip_elements(h, etree.Comment, 'script')
# ele_html = h.xpath('//div|//span')

# for each in ele_html:
#     print(html.tostring(each))
d = [
    {
        "app-period": "：令和5年2月9日（木） ～ 令和5年9月29日（金）※17時必着 （予算がなくなり次第、予告なく募集を終了します。） ・",
        "url": "https://www.mlit.go.jp/kankocho/page08_000145.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "応募受付期間",
                "similar-to": "応募受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "転入後3か月から1年以内（申請時には就業後3か月以上経過していること）",
        "url": "https://www.akkeshi-town.jp/izyuu/shienkin/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "工事請負契約又は売買契約締結の日から２ヶ月以内。",
        "url": "https://town.kochi-tsuno.lg.jp/section/post_1674",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "【申請時期】",
                "similar-to": "申請時期",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "大学の正規の最短修学年限",
        "url": "https://www.town.kuzumaki.iwate.jp:443/docs/2015111200360/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "貸与期間",
                "similar-to": "貸与期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "関係法令の施行から2か月後（令和2年6月30日）、または猶予を受けようとする税目の納期限のいずれか遅い日まで。",
        "url": "https://www.city.kanonji.kagawa.jp/site/coronavirus/23503.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-start": "令和4年度分国民年金保険料免除申請（特例措置）→令和4年7月1日から受付開始",
        "url": "https://www.city.miyakonojo.miyazaki.jp/site/coronavirus/20592.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "受付開始日",
                "similar-to": "受付開始日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "県から交付された特定不妊治療費助成事業承認決定通知書の交付日から1年以内",
        "url": "https://www.city.imabari.ehime.jp/neuvola/yosiki/tokuteifunin/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請の期間",
                "similar-to": "申請の期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "・施工業者との契約後速やかに（遅くても屋根工事完了前までに）申込書類を提出してください。 ・修繕、模様替えの場合は着工前一週間前までに申し込み書類を提出してください。",
        "url": "https://www.town.okinoshima.shimane.jp/www/sp/contents/1001000000165/index.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請時期",
                "similar-to": "申請時期",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和2年4月1日から令和5年3月31日 （請求期間が過ぎると第十一回特別弔慰金を受けることができなくなりますので、ご注意ください）",
        "url": "https://www.city.shiogama.miyagi.jp/soshiki/10/12786.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "請求期間",
                "similar-to": "請求期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "健康診査を受けた日から6か月以内",
        "url": "https://www.city.yamaguchi.lg.jp/site/kodomo/103125.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "◆申請期間",
                "similar-to": "申請期間",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和5年4月3日（月）から令和6年3月29日（金）まで ※ 1頭の猫に対して申請できるのは1回までです。 ※ 補助金交付予定額が予算に達した時点で締め切ります。",
        "url": "https://www.city.kawasaki.jp/350/page/0000017780.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-start": "令和4年（2022年）6月20日（月） ※先着順に受付し、予算額に達し次第、受付を終了します。 ※予算額には限りがありますので、申請をしても補助金の交付を受けられない",
        "url": "https://www.city.odawara.kanagawa.jp/field/disaster/bohan/prevention/p34064.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "申請受付開始日",
                "similar-to": "申請受付開始日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "申請は納期限までとなります。",
        "url": "https://www.town.gokase.miyazaki.jp/kakuka/choumin/973.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和5年2月28日まで",
        "url": "https://www.city.sagae.yamagata.jp:443/jigyou/jigyou/hojyoshien/ijuushienkin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 0.92,
                "ticked": True
            }
        }
    },
    {
        "app-end": "原則として納期限が到来する７日前までに申請してください。",
        "url": "https://www.town.nanbu.yamanashi.jp/kakuka/COVID-19/news/2021-0629-1254-1.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "太陽光受給契約確認書に記載された受給契約開始日から３ヶ月以内 です。 【 蓄電池 】 住宅用蓄電池システムを設置した方に、設置費用の一部を助成します。",
        "url": "https://www.city.miyako.iwate.jp/energy/renewableenergy_subsidies.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限は、",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和5 年4 月24日（月）～令和4年5月19日（金）",
        "url": "https://www.vill.otari.nagano.jp/www/contents/1001000000058/index.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和５年４月１日から令和６年３月３１日まで ※ただし、予算に達した時点で申し込みを締め切りますので、ご注意ください ■問い合わせ先",
        "url": "http://www.town.oto.fukuoka.jp/info/prev.asp?fol_id=2554",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "■申請期間",
                "similar-to": "申請期間",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-start": "福祉交流センター 2023年6月8日（木曜日）、2023年8月3日（木曜日） 午後1時～午後5時 2023年5月15日（月曜日）から",
        "url": "https://www.city.hamamatsu.shizuoka.jp/fukushisomu/welfare/seinennkoukenn/seinennkoukenn.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "申込開始日",
                "similar-to": "申込開始日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年8月31日 17時15分まで",
        "url": "https://www.city.inuyama.aichi.jp/1006634/1006777/1008440.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年6月22日 ～ 令和4年10月31日",
        "url": "https://www.town.minamiaizu.lg.jp/covid/2351.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "提出先",
        "url": "https://www.city.kasuga.fukuoka.jp/kosodate/eschool/shuugaku/1001726.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "受診をした月から、なるべく1年以内 ※ 申請できる権利は5年で消滅となります",
        "url": "https://www.town.shirosato.lg.jp/page/page000152.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年7月1日(金曜日)から令和5年2月28日(火曜日) (注意)郵送必着",
        "url": "https://www.vill.ohkura.yamagata.jp/hojokin_joseikin/mishugakujimuke/1124.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "課税年度の初日の属する年の１月３１日までに、固定資産税課税免除申請書及び必要書類を提出してください。",
        "url": "https://www.city.hagi.lg.jp/soshiki/29/h44374.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年2月4日(金曜日)から令和4年9月30日(金曜日)まで",
        "url": "http://www.town.shibecha.hokkaido.jp/kakuka/hokenhukushi/news/hikazei_setai_rinji_kyuufu.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和2(2020)年4月1日～令和5(2023)年3月31日",
        "url": "https://www.city.kadoma.osaka.jp/kenko_fukushi/chiiki_fukushi/2/10884.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "請求期間",
                "similar-to": "請求期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和９年３月３１日まで",
        "url": "https://www.town.aya.miyazaki.jp/site/iju/5645.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 0.92,
                "ticked": True
            }
        }
    },
    {
        "app-end": "骨髄等の提供が完了してから 90日以内 申請場所 健康福祉課成人健康係窓口 必要書類 以下のとおり 骨髄等提供者（ドナー）",
        "url": "https://www.town.kaminokawa.lg.jp/0014/info-0000000469-0.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期日",
                "similar-to": "申請期日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "申請期限は各期別の納期限と同日です。なお、 納期限を過ぎると減免の対象になりません。",
        "url": "http://www.rokkasho.jp/index.cfm/10,0,61,html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "検査日が令和4年4月1日～ 令和5年5月7日検査分 まで",
        "url": "https://kimotsuki-town.jp/bosai_anzen_1/kyukyu/kinnkyuusinngatakoronajyouhou/4845.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "受付終了",
                "similar-to": "受付終了日",
                "point": 0.93,
                "ticked": True
            },
            "app-period": {
                "keyword": "補助期間",
                "similar-to": "補助受付期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "年度をまたいで治療継続中の方は、治療実施翌年度の6月から3月末の期間",
        "url": "http://www.city.hioki.kagoshima.jp/boshi/kurashi/kosodate-kyoiku/kosodate/ninkatsu/funin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            },
            "app-period": {
                "keyword": "申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 0.92,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和5年3月31日までに申請してください。",
        "url": "https://www.kawabe-gifu.jp/?p=30518",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "第 1 回申請受付期間：平成 23 年12 月 1 日から平成 24 年3 月21 日",
        "url": "http://www.town.ama.shimane.jp/gyosei/torikumi/post-70.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "補助受付期間",
                "similar-to": "補助受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "・・・ 金融機関との協議による",
        "url": "https://www.city.hanyu.lg.jp/docs/2009060101762/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "貸付期間",
                "similar-to": "貸付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "検査を終了した日の属する年度末までに申請してください。",
        "url": "https://www.town.hatoyama.saitama.jp/hatonet/support/ninsinmae/kosodate_huninkensa.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "物件登録者 初めて登録された日から2年以内",
        "url": "https://www.city.oyama.tochigi.jp/site/akiyabank/212883.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "申請期間：令和4年7月4日（月曜日）～令和4年9月30日（金曜日） 申請は、先着順に受付いたします。 ただし、申請額が予算額を超えた日に複数の申請があった場合は、その日の申請人全員を対象とした抽選を別途行います。",
        "url": "http://www.city.matsuyama.ehime.jp/bosyu/ijuushakaishuushienn.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "清掃日又は11条検査受検日のいずれか遅い日の3か月後まで （遅れると申請ができません。）",
        "url": "https://www.city.koriyama.lg.jp/site/jougesuidou/5505.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請の時期",
                "similar-to": "申請時期",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-end": "は、8月11日（火曜日）までです。期限が迫っていますので、お早めに申請してください。8月12日以降は申請を受け付けることができなくなります。ご注意ください。",
        "url": "https://www.town.okuma.fukushima.jp/site/covid19/14192.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "：5月8日（金）～8月31日(月） ※オンライン申請は5月11日（月）から受付",
        "url": "http://www.vill-tenryu.jp/notice/administrative/corona_teigakukyufukin/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "５．受付期間",
                "similar-to": "受付期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-end": "対象品を購入した日（領収書に記載の日）の翌日から1年以内",
        "url": "https://www.city.katsushika.lg.jp/kenkou/1030182/1025594/1025595.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "平成25年2月8日（金）から平成25年2月21日（木）まで 意見受付期間 平成25年2月8日（金）から平成25年2月21日（木）まで",
        "url": "https://www.town.niseko.lg.jp/chosei/keikaku/sangyo/minkan_jutaku/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "意見受付期間",
                "similar-to": "受付期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "災害等による損害を受けた日から1年間",
        "url": "https://www.city.higashihiroshima.lg.jp/bosai/4/28925.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "【申請期間】",
                "similar-to": "申請期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "在学している学校の修業年限です。",
        "url": "http://www.town.sotogahama.lg.jp/bunka/kyoiku/shougakukin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "貸付の期間",
                "similar-to": "貸付の期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和5年5月8日（月曜日）～令和5年12月15日（金曜日）",
        "url": "https://www.city.masuda.lg.jp/kurashi_tetsuzuki/bosai/saigainisonaeru/3/5432.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "5．受付期間",
                "similar-to": "受付期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "災害を受けた日から30日以内",
        "url": "https://www.city.yashio.lg.jp/bohan_bosai/bosai/hissaisya/mimaikin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "請求期間",
                "similar-to": "請求期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "新築住宅=最長3年間（最大30万円）",
        "url": "https://www.city.miyama.lg.jp/s006/kurashi/090/030/010/20200108133000.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "補助期間",
                "similar-to": "補助受付期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-end": "就労奨励金",
        "url": "https://www.city.echizen.lg.jp/office/050/020/hoikusijosei.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "受付期間：令和5年10月31日（火曜日）まで",
        "url": "https://www.town.togitsu.nagasaki.jp/anzen_anshin/bosai/5582.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間・場所",
                "similar-to": "受付期間",
                "point": 0.86,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和5年4月1日から令和6年3月11日まで",
        "url": "http://www.town.aomori-nanbu.lg.jp/index.cfm/6,0,60,236,html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和４年５月１６日（月）から ※ただし、受け付けできる件数に限りがございますので、ご了承ください。",
        "url": "https://www.town.nagatoro.saitama.jp/life/%E4%BD%8F%E5%AE%85%E3%83%AA%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0%E8%B3%87%E9%87%91%E5%8A%A9%E6%88%90%E5%88%B6%E5%BA%A6/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "​損害を被った日の属する月の翌月初日から1年間",
        "url": "https://www.town.shimamoto.lg.jp/site/covid-19/1300.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請可能期限",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和5年4月1日から令和6年3月31日",
        "url": "http://www.city.kamagaya.chiba.jp/kurashi-tetsuzuki/sumai/kekkonsinseikatu.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "学生納付特例を希望するとき（決定までは、3～4ヵ月程度かかります）。 ※学生納付特例を受けていた人で、引き続き学生納付特例を希望する場合は、毎年4月～5月中に、再度申請が必要です。",
        "url": "https://www.city.kumamoto.jp/hpKiji/pub/detail.aspx?c_id=5&id=100&class_set_id=3&class_id=564",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期日・時期",
                "similar-to": "申請期日",
                "point": 0.86,
                "ticked": True
            }
        }
    },
    {
        "app-end": "出生日から３か月以内に保護者の方が申請手続きをしてください",
        "url": "https://www.vill.takagi.nagano.jp/doc/2022040100067/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "出生から3か月以内",
        "url": "https://www.town.nishiwaga.lg.jp/mokutekibetsudesagasu/ninshin_shussan/1941.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和４年６月１日から令和４年１０月３１日 午前９時から午後５時まで",
        "url": "https://www.town.minamioguni.lg.jp/gyousei/other/post_15.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 0.92,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和５ 年12月28日（必着）",
        "url": "https://www.city.tomi.nagano.jp/category/coronagenmen/151648.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "・申請期限",
                "similar-to": "申請期限",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和4年度分",
        "url": "https://www.city.sumoto.lg.jp/site/covid19/10027.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "ドナーが骨髄等の採取に伴う入院をして退院した日の翌日、中止者にあっては中止日から起算して1年以内",
        "url": "https://www.city.hamamatsu.shizuoka.jp/hokenk/iryo/kotsuzui/kotsuzui-hojo.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "申請は、運転免許証を返納してから3か月以内に行ってください。",
        "url": "https://www.city.toki.lg.jp/kurashi/bohan/1004663/1003975.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限等",
                "similar-to": "申請期限",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-end": "申請年度の1月末迄 ※転入日によっては申請できなくなる場合が有りますので、要件を満たした場合は早めの相談をお願いします。",
        "url": "https://www.town.yoshinogari.lg.jp/lifeinfo/soshiki/mirai/1/ijyu_teijyu/1829.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "保険税の減免を受ける場合は、納期限までに申請が必要です。 減免申請書等は以下のとおりです。郵送での申請をご希望する場合や、ご質問等は税務課国民健康保険税係までお願いします。",
        "url": "https://www.town.oirase.aomori.jp/site/singatakorona/sinngatakoronakokuhozeigennmenn.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限等",
                "similar-to": "申請期限",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-end": "お子さんの出生日の翌日から6カ月以内 その他 申請時点で大府市に居住されているか等を確認させていただく場合がありますのでご了承ください。。",
        "url": "https://www.city.obu.aichi.jp/1013328/1013829/1013871/1014277.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-start": "令和2年5月1日",
        "url": "https://www.town.rifu.miyagi.jp:443/gyosei/kurashi_tetsuzuki/nenkin_hoken/3/3016.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "申請の受付開始日",
                "similar-to": "申請の受付開始日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-start": "(1)受付期限は令和５年6月30日までです。(受付時間は午前8時30分から午後5時15分) ※期限までに申請が難しい場所は市民課生活係までお気軽にご相談ください。",
        "url": "http://www.city.nanyo.yamagata.jp/simin/3675",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "申請の受付",
                "similar-to": "申請の受付開始日",
                "point": 0.88,
                "ticked": True
            }
        }
    },
    {
        "app-period": "随時",
        "url": "https://www.town.kudoyama.wakayama.jp/bousai/chairudo.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            },
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "1または2のいずれか早い日までです。",
        "url": "https://www.city.kitanagoya.lg.jp/bousai/2100114.php",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請の期限",
                "similar-to": "申請期限",
                "point": 0.93,
                "ticked": True
            },
            "app-period": {
                "keyword": "申請の期限",
                "similar-to": "申請の期間",
                "point": 0.87,
                "ticked": True
            }
        }
    },
    {
        "app-end": "6月7日（水） 夕張太集落センター 378－5888 ５月15日(月)",
        "url": "https://www.town.nanporo.hokkaido.jp/health/child-care/vaccination/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申込み期限",
                "similar-to": "申込期限",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和2年4月1日～令和5年3月31日 (請求期間を過ぎると第十一回特別弔慰金を受けることができなくなりますので、ご注意ください。)",
        "url": "http://www.city.inazawa.aichi.jp/kenko_fukushi/chiikifukushi/1001574.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "請求期間",
                "similar-to": "請求期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "6月1日から11月30日まで ※1組織申請受付期間内1回の申請になります。 ※申請書一式は毎年5月下旬に横須賀市に結成を届出た「自主防災組織」の町内会・自治会長に配布します。",
        "url": "https://www.city.yokosuka.kanagawa.jp/0525/anzen/jisyubousai/bousaikizaihojyokin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 0.92,
                "ticked": True
            }
        }
    },
    {
        "app-period": "毎年4月1日～5月末（途中申請の場合は、翌年1月末まで随時受け付けますが、受付翌月からの援助となります。）",
        "url": "https://www.city.setouchi.lg.jp/site/kyouikuiinnkai/2317.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "治療を受けた月の属する年度内（4月1日から翌年3月31日まで） とします。",
        "url": "http://www.town.toei.aichi.jp/1140.htm",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請時期",
                "similar-to": "申請時期",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "平成30年４月から 申請は各年度の初回のみ必要で、以後は支給額がある場合に、指定振込先へ振り込みます。 初回申請以降は毎年７月に申請が必要です。",
        "url": "https://www.city.fukuoka.lg.jp/fukushi/shisetsushien/health/sevice/sinkougaku.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "随時",
        "url": "https://www.town.aichi-togo.lg.jp/iryo_kenko_fukushi/iryo_kenko/7813.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請等の時期",
                "similar-to": "申請時期",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-start": "・6月10日（金曜日）から受付を開始します。 なお、保険料の減免決定通知が届くまでは、保険料のご納付をお願します。 ※新型コロナウイルス感染症予防のため申請は郵送でも受付けをします。",
        "url": "https://www.city.shunan.lg.jp/site/singatakorona/52657.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "申請の受付",
                "similar-to": "申請の受付開始日",
                "point": 0.88,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和５年３月３１日（金）",
        "url": "https://www.town.miyaki.lg.jp/kenko/josei/_1068.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "２．申請期限",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-end": "所管(国・県・市など) 問合せ(電話) ホームページ",
        "url": "https://www.city.ishigaki.okinawa.jp/about_covid19_ishigaki_1/7536.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "不妊治療費事業受診等証明書に記載された治療期間終了日後1年以内に申請してください。 期限を過ぎた場合、助成金の支給はできません。",
        "url": "http://www.vill.oshino.lg.jp/docs/2013010702879/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "・令和４年１２月３１日（土）まで",
        "url": "https://www.iinan.jp/site/ncov/2442.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "【申請期限】",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "随時受け付けています。 予算に達し次第終了となります。",
        "url": "https://www.city.kobayashi.lg.jp/boshuosagasu/sonohokanoboshu/4133.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "原則として、建物登記完了日の翌日から起算して2カ月以内",
        "url": "https://www.town.oi.kanagawa.jp/site/iju/jutakushutoku-hojokin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "1期 令和5年5月15日(月) ※締め切りました。",
        "url": "https://www.town.atsuma.lg.jp/office/employment/job/entrepreneur/subsidies_grants/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申し込み期限",
                "similar-to": "申込期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "禁煙外来治療終了日から1年以内の申請に限ります",
        "url": "https://www.city.komatsu.lg.jp/kenko_fukushi/4/4/5089.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和2年2月1日から令和5年3月31日までに納期限が到来する保険税が減免の対象となります。",
        "url": "http://www.shinchi-town.jp/site/covid-19/kokuhocoronagenmen.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "申請時期：本市に転入し上記に掲げる、「移住元要件」「移住先要件」及び「地域の担い手としての役割に関する要件」を満たした後。",
        "url": "https://www.city.annaka.lg.jp/gyousei/kikaku_seisaku/ijyuu-shienkin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間：随時",
                "similar-to": "受付期間",
                "point": 0.86,
                "ticked": True
            }
        }
    },
    {
        "app-period": "○4月1日～ 先着順 予算枠に達ししだい終了となります。 ○補助金交付決定は、4月中旬以降の予定です。 （申請様式等は下方にあります。↓）",
        "url": "https://www.city.aki.kochi.jp/life/dtl.php?hdnKey=2440",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "▽申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 0.87,
                "ticked": True
            }
        }
    },
    {
        "app-end": "減免を受けようとする納期限までに申請が必要 ３．申請に必要な書類 ア 申請する全ての方 ・個人市民税・県民税減免申請書 ・本人確認書類",
        "url": "https://www.city.uruma.lg.jp/kurashi/108/775/23669",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "２．申請期限",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "2022年4月15日(金曜日)～2023年3月31日(金曜日)まで。",
        "url": "https://www.city.kamisu.ibaraki.jp/business/chusho/1002793/1002794.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "補助金交付申請期限",
        "url": "https://www.city.niigata.lg.jp:443/business/kigyo/kigyo_annai/supporttop/2022officebiru.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "指定申請期限",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和4年8月4日（木曜日）当日消印有効",
        "url": "http://www.city-kirishima.jp/anshin/higaisyashien.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "応募締切：",
                "similar-to": "応募締切",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-end": "手術日より3カ月以内 です。",
        "url": "https://www.city.tomioka.lg.jp/www/contents/1522204408829/index.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限は、",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "奨学金の貸与が決まった年度の４月から在学する学校の正規の修学期間",
        "url": "https://www.vill.samegawa.fukushima.jp/page/page000176.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "貸与期間",
                "similar-to": "貸与期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "毎年 年度末 3月20日まで（休日の場合は前日）",
        "url": "https://www.vill.yasuoka.nagano.jp/docs/2518.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "6月21日",
        "url": "http://www.town.nose.osaka.jp/kurashi/kenko/4858.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "受付終了",
                "similar-to": "受付終了日",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-period": "医学生 6年以内",
        "url": "https://www.city.fuchu.hiroshima.jp/fukushi_kenko/iryo_byoin/2041.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "貸付期間",
                "similar-to": "貸付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和2年4月1日から令和5年3月31日",
        "url": "https://www.city.tagajo.miyagi.jp:443/fukushi/kenko/fukushi/tyouikin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "請求期間",
                "similar-to": "請求期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "治療が終了した日の属する年度の3月31日まで。（ただし、2月～3月治療終了分は翌年度の4月最終開庁日まで）",
        "url": "https://www.town.kouhoku.saga.jp/kiji003748/index.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和6年3月29日（金曜日）まで（書類必着）",
        "url": "https://www.city.numazu.shizuoka.jp/deai/shien/index.htm",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 0.92,
                "ticked": True
            }
        }
    },
    {
        "app-period": "高校入学前の中学3年時の3月 （※詳しい日程については、毎年、中学3年生を対象に配布する募集案内に記載します。）",
        "url": "https://www.city.hakusan.lg.jp/bunka/gakko/1002106.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請時期",
                "similar-to": "申請時期",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "支給申請期限は2年となっています。",
        "url": "https://www.town.ando.nara.jp/0000000009.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "［申請期限］",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和５(2023)年４月3日（月）から令和６(2024)年３月29日（金）まで",
        "url": "http://www.city.aichi-miyoshi.lg.jp/bosai/3herumetto-hozyokinn.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            },
            "app-period": {
                "keyword": "補助申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和6年3月31日まで",
        "url": "http://www.town.hidaka.hokkaido.jp/site/kosodate/hukushi-hunintiryo.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期日",
                "similar-to": "申請期日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "平成29年10月31日（平成30年3月30日まで完了届を提出できること） ※秋田県の住宅リフォーム推進事業と併用ができます。",
        "url": "https://www.city.semboku.akita.jp:443/news_topics/whatsnew.php?id=1872",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申込期限",
                "similar-to": "申込期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和5年度の申請は、 令和6年1月31日（水）まで です。 予算に限りがあるため、申請要件を満たしている場合はお早めにご相談ください。",
        "url": "http://www.town.kannami.shizuoka.jp/gyosei/ijuu-teijuu/ta11002020.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "建物登記完了日または松田町に住民登録をした日のいずれか遅い日から ６カ月以内 に申請してください。",
        "url": "https://town.matsuda.kanagawa.jp/site/teiju-syoushi/h26koufuseido.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和5年5月1日（月）から令和6年2月23日（金）まで",
        "url": "https://www.city.hirosaki.aomori.jp/kurashi/akiya/2015-1008-1749-45.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "２．申請期間",
                "similar-to": "申請期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年9月30日（金曜日） ※当日消印有効",
        "url": "https://www.town.takanabe.lg.jp/emergency/3549.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "貸与を受けた年度の3月末日まで",
        "url": "https://www.city.nikko.lg.jp/gakkou/shouchuu/tetsuzuki/jun-youhogo.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "貸与期間",
                "similar-to": "貸与期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "補正具を購入した日から1年以内",
        "url": "https://www.town.ginan.lg.jp/3389.htm",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和５年４月１日より補助金額が変更となります。",
        "url": "https://www.city.odate.lg.jp/city/handbook/handbook10/page47/p432",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和４年４月３０日（土曜日）消印有効 ※窓口での申請は令和４年４月２８日（木曜日）まで",
        "url": "https://www.town.sakae.chiba.jp/page/page005506.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "●申請期限",
                "similar-to": "申請期限",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-start": "平成31年4月1日〜",
        "app-end": "避妊・去勢手術日から3か月以内",
        "url": "https://www.town.tohnosho.chiba.jp/hojokin_joseikin/doubutu/2843.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "申請受付",
                "similar-to": "申請受付開始日",
                "point": 0.86,
                "ticked": True
            },
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "4月1日から受け付けます。その年度の3月31日までに完了する事業が対象です。",
        "url": "https://www.city.mizunami.lg.jp/1004458/1004577/1006624.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和3年3月31日まで",
        "url": "https://www.town.otsuchi.iwate.jp/gyosei/docs/374452.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "【申請期限】",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "年度当初の認定の場合、在校生は1月～2月、新1年生は4月上旬までです。 年度途中に生活状態が悪化した場合は、随時受け付けます。",
        "url": "https://www.town.tobe.ehime.jp/soshiki/10/syuugakuenjyo.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請時期",
                "similar-to": "申請時期",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "児童手当は、原則、申請した月の翌月分から支給されます。ただし、出生日や転出予定日（異動日）が月末に近い場合、申請が翌月になっても異動日の翌日から15日以内の申請であれば、申請月から支給します。申請が遅れると、遅れた月分の手当を受けられなくなることがありますので、ご注意ください。",
        "url": "https://www.city.osaka.lg.jp/kodomo/page/0000370608.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期日",
                "similar-to": "申請期日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年12月1日から令和5年1月31日まで（消印有効）",
        "url": "https://www.pref.yamanashi.jp/ch-hokenf/57252305431.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間：",
                "similar-to": "受付期間",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年11月30日まで （受付は終了しました）",
        "url": "https://www.town.saka.lg.jp/2000/10/08/post_720/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和２年４月１日から令和５年３月３１日まで （請求期間を過ぎると第十一回特別弔慰金を受けることができなくなりますので、ご注意ください。）",
        "url": "https://www.city.otsuki.yamanashi.jp/gyoumu/06fukushikaigo/senbotsushaizokutokubetsuchouikin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "請求期間",
                "similar-to": "請求期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "開庁時間内 随時",
        "url": "https://www.city.asakura.lg.jp/www/contents/1297153401079/index.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "定期券購入日から３０日以内",
        "url": "https://www.town-kofu.jp/2/1/11/7/4/01/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "毎年3月～ 4月(詳しくは、市のHPでお知らせします。)",
        "url": "https://www.hyugacity.jp/display.php?cont=140312112439",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "◎受付期間",
                "similar-to": "受付期間",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-end": "不妊治療費事業受診等証明書に記載された治療期間終了日後1年以内に申請してください。 期間を過ぎた場合、助成金の支給はできません。",
        "url": "https://www.vill.tabayama.yamanashi.jp/gyousei/2016-0607-1428-1.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和2年4月1日から令和5年3月31日 （請求期間を過ぎると第十一回特別弔慰金を受けることができなくなりますので、ご注意ください）",
        "url": "http://www.town.kinko.lg.jp/fukushi-h/dai11kaitokubetucyouikin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "請求期間",
                "similar-to": "請求期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "介護職員初任者研修修了日の翌日から1年以内",
        "url": "https://www.city.fujioka.gunma.jp/kenko/koreishafukushi_kaigo/2848.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "就職活動を行った日から6か月以内",
        "url": "https://www.city.minamisoma.lg.jp/portal/business/jigyoshoshien/2/12188.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "・犯罪行為による死亡若しくは傷病の発生を知った日から２年以内又は死亡若しくは傷病が発生した日から７年以内",
        "url": "https://www.city.iwanuma.miyagi.jp:443/bosai/bosai-bohan/bohan/hannzaihigaisyatousienn.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "●申請期限",
                "similar-to": "申請期限",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和5年3月15日まで",
        "url": "https://www.town.kawasaki.miyagi.jp/site/covid-19/217.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "※申請期限",
                "similar-to": "申請期限",
                "point": 0.93,
                "ticked": True
            }
        }
    },
    {
        "app-period": "学校における正規の修学期間",
        "url": "https://www.town.yamada.iwate.jp/docs/1013.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "貸与期間",
                "similar-to": "貸与期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-start": "令和２年５月１日",
        "url": "http://www.town.yakushima.kagoshima.jp/info-living/27828/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "申請の受付開始日",
                "similar-to": "申請の受付開始日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年度分 は、 令和4年度末 に資格を取得したことになどより、 令和5年4月以後に納期限 が設定されているもの。",
        "url": "https://www.city.kameoka.kyoto.jp/site/covid-19/3090.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和5年8月31日（木曜日）まで",
        "url": "https://www.vill.iitate.fukushima.jp/soshiki/1/7959.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和3年度非課税世帯： 令和4年9月30日（金曜日）",
        "url": "http://www.town.wakuya.miyagi.jp/faq/kenko/fukushi/20220128.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "申込書：申込み期限 住宅の引き渡しの概ね１０日前まで（住宅の引渡し時点で申込書の受理通知が発行されていること） 申請書：申請期限",
        "url": "https://www.pref.kochi.lg.jp/shinsei_todokede_hojokin/shinsei_todokedeyoshiki/2014032700799/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "毎年7月分～次年6月分 毎年7月1日から、随時申請できます。",
        "url": "https://www.city.sakuragawa.lg.jp/sp/kurashi/tetsuzuki/nenkin/page000092.html",
        "tried": 2,
        "status": 200,
        "redirected": True,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "奨励措置期間は課税年度から10年以内とする。",
        "url": "https://www.akiota.jp/site/ijyu/1083.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "補助期間",
                "similar-to": "補助受付期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和5年5月22日(月曜日)から令和5年9月29日(金曜日)",
        "url": "https://www.city.tamana.lg.jp/q/aview/137/8231.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和５年４月１７日から 令和５年１１月３０日まで",
        "url": "http://www.city.takahashi.lg.jp/soshiki/22/reform-hojokin.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "治療の種類によって申請期間が異なります（年度内申請ではなくなりました）。 ＊やむを得ない理由で申請期限を過ぎてしまう場合は、あらかじめ保健相談センターへご連絡ください。",
        "url": "https://www.vill.shinto.gunma.jp/education/000144/000148/p000171.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和4年7月15日（金曜日）～令和5年5月31日（水曜日）必着",
        "url": "https://www.city.higashiyamato.lg.jp/kurashi/nenkin/1001896/1001902.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "原則3か月以内（状況に応じて3か月以内での延長貸付や再貸付が受けられる場合あり） 注 要相談",
        "url": "https://www.city.hanamaki.iwate.jp/1011531/1013866/1013867/1014233.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "貸付期間",
                "similar-to": "貸付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年3月31日まで",
        "url": "https://www.town.hirogawa.wakayama.jp/juumin/2020-0629-1811-9.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和2年4月1日から 令和5年3月31日 まで（期間を過ぎると請求ができませんのでご注意ください）",
        "url": "http://www.city.wako.lg.jp/home/fukushi/chiikifukushi/_19284.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "請求期間",
                "similar-to": "請求期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和７年３月31日まで(必着)",
        "url": "https://www.city.amakusa.kumamoto.jp/kiji0031011/index.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "【申請期間】",
                "similar-to": "申請期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-end": "購入後60日以内に申請してください。",
        "url": "http://www.uenomura.jp/admin/education/kosodate/childseat.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和2年5月25日(月)～令和2年9月25日(金) ※土日祝日を除く8時30分～17時15分 申請先 上士幌町役場保健福祉課福祉担当窓口(郵送申請も可)",
        "url": "https://www.kamishihoro.jp/entry/00004346",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和3年(2021年)4月1日（木曜日)〜令和4年(2022年)3月31日(木曜日)",
        "url": "https://www.city.satte.lg.jp/sitetop/life_cityadmin/municipal_administration/7/7/3588.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            },
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和3年5月19日（水曜日）から令和4年2月28日（月曜日）まで",
        "url": "https://www.vill.itsuki.lg.jp/kiji0031259/index.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請受付期間",
                "similar-to": "補助申請受付期間",
                "point": 0.92,
                "ticked": True
            }
        }
    },
    {
        "app-period": "最後の妊婦健康診査受診日から6カ月以内",
        "url": "https://www.city.kashiwazaki.lg.jp/benri_service/sinseidownload/shinseishodownload/kosodate_kyoiku/2/16464.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請時期",
                "similar-to": "申請時期",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-start": "令和2年5月1日",
        "url": "https://www.town.kitahiroshima.lg.jp/site/2019-ncov/18620.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-start": {
                "keyword": "受付開始日",
                "similar-to": "受付開始日",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "申請期限はありません。",
        "url": "https://www.town.mamurogawa.yamagata.jp/docs/2018120100546/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "随時",
        "url": "https://www.city.ikoma.lg.jp/0000000011.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年8月1日月曜日から",
        "url": "https://www.city.inzai.lg.jp/0000000294.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "受付期間",
                "similar-to": "受付期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "・1年間の診療分について、診療期間終了後の 3か月以内 までに申請を行う。",
        "url": "https://www.town.hakone.kanagawa.jp/www/contents/1100000000655/index.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "【申請期間】",
                "similar-to": "申請期間",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和元年 ８月１日 （木）～ 令和２ 年２月３日（月）",
        "url": "https://www.city.nago.okinawa.jp/articles/2019071000015/",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "助成対象講座を修了した日から3か月以内",
        "url": "https://www.city.ibaraki.osaka.jp/hojokin_joseikin/jigyosha_sangyo/koyo_shugyo/56523.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和5年6月30日（消印有効）",
        "url": "https://www.city.saitama.jp/001/002/001/p081397.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "申請期限",
                "similar-to": "申請期限",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-period": "毎年4月1日から3月31日まで",
        "url": "https://www.city.fukuchiyama.lg.jp/site/bousai/1831.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "資格取得日または結果通知日から３カ月以内。 また、補助金交付額が予算額に到達した場合、その年度内の申請を打ち切ります。",
        "url": "https://www.city.niimi.okayama.jp/business/business_detail/index/226.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "＜申請期限＞",
                "similar-to": "申請期限",
                "point": 0.89,
                "ticked": True
            }
        }
    },
    {
        "app-period": "令和4年7月中旬の賦課決定通知書到着後から令和5年3月31日（当日消印有効）",
        "url": "https://www.city.akabira.hokkaido.jp/docs/1724.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-period": {
                "keyword": "申請期間",
                "similar-to": "申請期間",
                "point": 1.0,
                "ticked": True
            }
        }
    },
    {
        "app-end": "令和5年度当初の申請の場合、令和5年2月22日（水曜日）までに、申請書をお子さんの通学校または学校教育課に提出してください。",
        "url": "https://www.city.ishikari.hokkaido.jp/site/kyouiku/14794.html",
        "tried": 1,
        "status": 200,
        "redirected": False,
        "detail": {
            "app-end": {
                "keyword": "提出期日",
                "similar-to": "提出期日",
                "point": 1.0,
                "ticked": True
            }
        }
    }
]
starts = []
ends = []
pers = []
ob = {
    'app-start': starts,
    'app-end': ends,
    'app-period': pers
}

for each in d:
    for key in ob:
        if key in each:
            ob[key].append(each[key])
            
for key in ob:
    f = open(f'test{key}.json', 'w')
    f.write(
        json.dumps(
            ob[key],
            indent=4,
            ensure_ascii=False
        )
    )
    f.close()
