from django.shortcuts import render
from util_demian import utils
from appointment.templatetags.appointment_tags import make_post_context

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

# 필수 ['hero', True, 'Hero', False],
components_mentor_ds = [
    ['popup', False, None, None],
    ['counts', True, 'Counts', True],
    ['about', True, 'About', True],
    ['whyus', True, 'Why Us', True],
    ['testimonials', True, 'Testimonials', True],
    ['team', True, 'Teacher', True],
    ['faq', True, 'FAQ', True],
    ['courses', True, 'Courses', True],
    ['features', True, 'Features', True],
    ['events', True, 'Events', True],
    ['pricing', True, 'Pricing', True],
    ['contact', True, 'Contact', True],

    # 특수목적 컴포넌트의 사용여부
    ['lang', False, None, None],

]


def home(request, lang=None):
    mytheme = "mentor_ds"
    context = {
        'components': components_mentor_ds,

        "color": "default",
        "theme": mytheme,
        "naver": "https://booking.naver.com/booking/13/bizes/441781",
        "use_logo": False,

        "seo": {
            "company_name": "MyEnglish",
            "url": "myenglishkr.com",
            "small_title": "1:1 Speaking Practice",
            "desc": "강남구 서초동 교대 반포 법조타운 위치 내인생치과의 홈페이지, 삼성서울병원 구강외과 전문의 진료",
            "keywords": "내인생치과, 반포대로치과, 교대교정치과, 반포치과, 서초치과, 서초동치과, 교대역치과 "
        },
        'analytics': {
            'google_id': "G-351NZ2S4F9",
            'naver_id': "feadf9e1b55868"
        },
        "font_link": "https://fonts.googleapis.com/css2?family=Gugi&family=Jua&family=Nanum+Pen+Script&family=Noto+Sans+KR:wght@100;300;400;500;700;900&family=Noto+Serif+KR:wght@200;300;400;500;600;700;900&display=swap",


        "social": {
            "facebook": "https://blog.naver.com/mylife2879",
            "twitter": "https://blog.naver.com/mylife2879",
            "instagram": "https://blog.naver.com/mylife2879",
            "youtube": "https://blog.naver.com/mylife2879",
            "blog": "https://blog.naver.com/mylife2879",
        },

        'get_started': 'courses',

        "basic_info": {
            "company_name": "MyEnglish",
            "owner": "Kevin Shim",
            "business_reg_number": "439-56-00511",
            "phone": "02-521-2879",
            "addr": "서울 서초구 반포대로30길 82 2층 201호<br>(서초구 서초동 1574-1)",
            "owner_email": "kevin.shim@myenglishkr.com",
            "consult_email": "kevin.shim@myenglishkr.com"
        },

        "about": {
            "title": "믿음을 주는 것은 의사의 몫입니다.",
            "subtitle": "저,환자,그리고 직원 모두 최고로 만족할 수 있는 우리들의 '인생' 치과가 되었으면 좋겠습니다.",
            "head": "저는 경희대학교를 졸업하고 삼성서울병원에서 구강외과레지던트를 수련받고 구강외과 전문의 자격증을 취득하였습니다. 다양",
            "contents": [
                "<strong>과잉진료나 허위진료를 하지 않습니다.</strong><br>현재 환자분의 상태에 대해 충분히 설명하고 필요한 치료를 진행합니다.",
                "<strong>책임을 가진 의료진이 진료합니다.</strong><br>대표원장이 주치의로서 환자분을 책임지고 진료하고 있습니다."
            ],
            "tail": "치과 이름과 같이 제 인생에 있어서 마지막 치과이면서 20여 년의 임상경험으로 환자분들에게 최고의 만족을 드려 ‘인생치과’가 될수 있도록 최선을 다해 다음의 약속을 치키도록 하겠습니다.",
            "image_filename": "about.jpg",
            "video_link": "https://www.youtube.com/watch?v=vu34oUFP_SA",
        },

        "gallery": {
            "title": "Gallery",
            "desc": "Photos from Our Clinic",
        },

        "faq": [
            {
                "q": "수업은 어디서 진행되나요?",
                "a": "일대일 수업의 경우, 편안한 분위기를 선호하는 학습자는 카페에서, 조용한 공간을 선호하는 학습자는 스터디룸에서 진행됩니다. 현재 모든 수업은 강남역과 삼성역 사이에서 진행되고 있습니다. Skype 및 Zoom 을 통한 온라인 수업도 가능합니다."
            },
            {
                "q": "클래스는 어떻게 진행되나요?",
                "a": "수업 중에 선생님은 학생에게 다양한 주제에 대해 질문하고 문법적 오류, 새로운 어휘 및 표현 등을 체크하며 자연스러운 대화를 이어갑니다. 체크된 내용들은 레슨노트로 작성되어 수업 후 학생의 이메일로 전송됩니다.<br>시험, 면접, 발표 준비 수업의 경우 자연스러운 대화 스타일에서 모의 면접 스타일로 초점이 바뀝니다. 학생들은 수업에서 새로운 어휘, 표현 및 수정된 문장을 연습할 수 있습니다. 일반적으로 수업에서 학생은 70~80%를, 교사는  20~30%를 이야기합니다."
            },
            {
                "q": "초보자도 클래스를 신청할 수 있나요?",
                "a": "영어회화 경험이 없는 초보자도 환영합니다! 물론 대화 시작 전에 기본적인 어휘와 문장 패턴에 대한 기본 학습이 진행될 것입니다. 수업 때 선생님은 영어만 사용하나 초보자들을 위해 필요시 한국어를 사용할 수 도 있습니다. 학생들이 표현하려고 하는 것을 표현할 수 있는 매우 편안한 분위기가 될 것입니다. 실수를 하거나 완벽판 표현을 할 수 없는 것은 지극히 정상적이고 자연스러운 일입니다. 이것은 초보자들뿐만 아니라 모든 레벨의 학습자 모두 마찬가지입니다."
            },
            {
                "q": "클래스를 위한 준비물이 있나요?",
                "a": "네! 수업에는 영어로 말하고자하는 열정과 스피킹 능력을 향상시키고 싶다는 마음만 가지고 오시면 됩니다."
            },
            {
                "q": "번역 또는 통역서비스도 제공하나요?",
                "a": "현재 통역, 번역수업은 없습니다. 그러나, 영어 문장은 수업 시간에 교정할 수 있습니다. 교정 가능한 문서로는 논문, 비즈니스 이메일, 대학 과제, 발표 스크립트 등이 있습니다."
            },
            {
                "q": "온라인 클래스도 있나요?",
                "a": "Skype 및 Zoom 수업이 가능합니다. 모든 수업은 온라인 수업으로 대체 가능합니다.  온라인 수업은 대면 수업과 같은 방식으로 진행되며, 레슨 노트와 수업 자료는 화면으로 공유됩니다."
            }
        ],

        "services": {
            "title": "서비스",
            "subtitle": "서브타이틀",
            "type": "icon",
            "items": [
                {
                    "image_filename": "1.png",
                    "icon": "fa-stethoscope",  # bxl-dribbble
                    "title": "어려운 케이스 및 당일 사랑니 발치 수술이 가능합니다.",
                    "desc": "대학병원으로 의뢰하는 다양한 고난이도의 사랑니를 20여년 경력의 구강외과 전문의가 발치합니다."
                },
                {
                    "image_filename": "3.png",
                    "icon": "fa-hospital",
                    "title": "편리한 접근성으로 내원이 용이합니다.",
                    "desc": "교대역 출구 1분 거리에 위치해 있어 찾기가 쉽고 대중교통 이용시 접근성이 편리합니다."
                },
                {
                    "image_filename": "4.png",
                    "icon": "fa-hand-sparkles",
                    "title": "한차원 높은 소독시스템.",
                    "desc": "핸드피스 전용 소독기와 모든 체어 및 대기실에 LED 공간 표면 살균기 가동 "
                }
            ]
        },

        "team": {
            "title": "닥터",
            "subtitle": "닥터",
            "type": "desc",  # career or desc
            "members": [
                {
                    "name": "김형진",
                    "title": "대표원장",
                    "desc": "Magni qui quod omnis unde et eos fuga et exercitationem. Odio veritatis perspiciatis quaerat qui aut aut aut",
                    "career": [
                        "구강악안면외과 국가전문의",
                        "삼성서울병원 구강외과 전공",
                        "삼성서울병원 치과진료부 외래교수",
                        "대한구강악안면성형외과학회 인정의",
                        "원광대학교 치과대학 졸업",
                        "EAO(유럽임플란트학회) 정회원",
                        "대한치과보철학회 정회원",
                        "삼성서울병원 교정과 Residency course",
                        "Osstem AIC 임상지도의"
                    ],
                    "certs": [
                        "치과의사전문의자격증",
                        "구강악안면성형외과자격증",
                        "오스템지도의",
                        "삼성서울병원외래교수"
                    ],
                    "social": {
                        "twitter": "https://blog.naver.com/mylife2879",
                        "facebook": "https://blog.naver.com/mylife2879",
                        "instagram": "",
                        "linkedin": "",
                    },
                },
                {
                    "name": "설정은",
                    "title": "부원장",
                    "desc": "Magni qui quod omnis unde et eos fuga et exercitationem. Odio veritatis perspiciatis quaerat qui aut aut aut",
                    "career": [
                        "카톨릭대학교 치아교정학 전공",
                        "삼성서울병원 치과진료부 외래교수",
                        "부산대학교 치의학과 졸업",
                        "대한 치아교정학회 정회원",
                        "대한 심미치과학회 정회원",
                        "인비절라인(INVISALIGN) 인증의",
                        "인코그니토(INCOGNITO) 인증의"
                    ],
                    "certs": [
                        "치과의사전문의자격증",
                        "구강악안면성형외과자격증",
                        "오스템지도의",
                        "삼성서울병원외래교수"
                    ],
                    "social": {
                        "twitter": "",
                        "facebook": "",
                        "instagram": "https://blog.naver.com/mylife2879",
                        "linkedin": "https://blog.naver.com/mylife2879",
                    },
                }
            ]
        },

        "contact": {
            "desc": "3호선, 8호선 가락시장역 2번출구 잠실방향으로  도보로 2분 거리에 위치",
            "google_map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3165.53885481917!2d127.11330765109818!3d37.49520717971214!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x357ca593b8c5f7ef%3A0xc814cf4db2f054ea!2z6rCA65297IK87ISx7LmY6rO87J2Y7JuQ!5e0!3m2!1sko!2skr!4v1648771966798!5m2!1sko!2skr",
            "address": "서울시 송파구 양재대로",
            "phone": "02-431-2804",
            "noti": {
                "title": "Parking",
                "desc": [
                    "가락시장 가락몰 주차장 이용(2시간 주차지원)",
                    "네비게이션 : 서울웨딩타워 검색",
                ]
            },
            "timetable": {
                "title": "진료시간",
                "desc": {
                    "월수금": "09:00 am – 06:00 pm",
                    "화(야간)": "09:00 am – 08:00 pm",
                    "토": "10:00 am – 02:00 pm",
                    "점심시간": "012:30 pm – 01:30 pm"
                },
                "note": [
                    "<span class='text-primary'>목요일</span>은 휴진입니다.",
                    "<span class='text-primary'>토요일</span>은 점심시간 없이 진료합니다.",
                ]
            }
        },

        "whyus": {
            "major": {
                "title": "치과전문의 진료",
                "contents": [
                    "구강악안면외과와 교정과를 전공한 원장님들의 특화된 진료를 제공합니다.",
                    "삼성서울병원과의 유기적인 협력관계로 신속한 연계가 가능합니다. (대표원장 현 삼성서울병원 외래교수 재직)",
                    "삼성서울병원과의 유기적인 협력관계로 신속한 연계가 가능합니다. (대표원장 현 삼성서울병원 외래교수 재직)"
                ],
                "link": "#doctors"
            },
            "_comment_type": "icon or image",
            "type": "icon",

            "_comment_icon": "https://boxicons.com/ [bx-group, bx-pulse, bx-buildings, bx-bed]",
            "minor": [
                {
                    "icon": "bx-buildings",
                    "title": "상급병원과의 연계",
                    "contents": "삼성서울병원과의 유기적인 협력관계로 신속한 연계가 가능합니다. (대표원장 현 삼성서울병원 외래교수 재직)"
                },
                {
                    "icon": "bx-pulse",
                    "title": "당일 사랑니발치",
                    "contents": "치과용 CT를 이용한 정밀검사를 통해 수술이 필요한 사랑니도 발치가 가능합니다."
                },
                {
                    "icon": "bx-bed",
                    "title": "수면진정치료",
                    "contents": "치과공포증으로 치료가 어려웠던 환자분들도 안전하고 편안하게 수면진정치료를 받으실 수 있습니다."
                }
            ]
        },

        "testimonials": {
            "subtitle": "What are they saying",
            "stories": [
                {
              "photo": "testimonials-1",
              "name": "Hyungjin Kim",
              "job": "Dentist",
              "desc": "훌륭하고 친절한 선생님과 좋은 내용의 커리큘럼입니다."
            },
            {
              "photo": "testimonials-2",
              "name": "Jungeun Seol",
              "job": "Ceo &amp; Founder",
              "desc": "훌륭하고 친절한 선생님과 좋은 내용의 커리큘럼입니다."
            }
          ]
        },

        "cta": {
            "title": "카카오톡 상담",
            "desc": "카카오톡을 통해 상담 및 예약 가능합니다.",
            "link": "http://pf.kakao.com/_xexhxgxlV"
        },

        "clients": ["amc", "cmc", "khmc", "pnuh", "sev", "smc"],

        'lang': {
            'list': ['kor', 'eng'],
            'selected': lang,
        },
        "portfolio": {
            'title': "CASES",
            'subtitle': '주목할 만한 치과 케이스 모음',
        },

        "courses": [
            {
                "photo": "course-1",
                "field": "English",
                "price": "20000원",
                "title": "Practical Conversations - General",
                "desc": "With an endless amount of conversation topics such as traveling, shopping, cooking, work, culture, small talk, movies and music just to mention a few, work on your self-expression skills as you practice giving your opinions on a variety of subjects using related material.",
                "member": ["member1", "Kevin Shim"],
                "user": 6,
                "heart": 6
            },
            {
                "photo": "course-2",
                "field": "English",
                "price": "50000원",
                "title": "Practical Conversations - Business",
                "desc": "The language we use with our managers at work, overseas clients, and in professional emails is different from the type of language we use with our friends. Learn more about vocabulary and phrases common in the workplace with business speaking classes.\n",
                "member": ["member1", "Kevin Shim"],
                "user": 6,
                "heart": 6
            },
            {
                "photo": "course-3",
                "field": "English",
                "price": "10,000원",
                "title": "Interview & Presentation Prep",
                "desc": "Practice being able to talk about your resume off-script during an interview so your interviewer knows you haven't simply memorized your answers. Learn about both the cultural and linguistic differences regarding presentations in front of a multicultural audience.",
                "member": ["member1", "Kevin Shim"],
                "user": 6,
                "heart": 6
            },
            {
                "photo": "course-4",
                "field": "English",
                "price": "10,000원",
                "title": "Test Prep - OPIC, IELTS, TOEIC, TOEFL (speaking section)",
                "desc": "In test prep classes, you will have the opportunity to go over common questions during the speaking sections of English proficiency tests in Korea. Practice giving your answers clearly and impressing the scorers with great vocabulary and native-like expressions.",
                "member": ["member1", "Kevin Shim"],
                "user": 6,
                "heart": 6
            }
        ],
        "features": [
            {
                "icon": "ri-store-line",
                "title": "Lorem Ipsum",
                "link": ""
            },
            {
                "icon": "ri-bar-chart-box-line",
                "title": "Dolor Sitema",
                "link": ""
            },
            {
                "icon": "ri-calendar-todo-line",
                "title": "Sed perspiciatis",
                "link": ""
            },
            {
                "icon": "ri-paint-brush-line",
                "title": "Magni Dolores",
                "link": ""
            },

            {
                "icon": "ri-database-2-line",
                "title": "Nemo Enim",
                "link": ""
            },
            {
                "icon": "ri-gradienter-line",
                "title": "Eiusmod Tempor",
                "link": ""
            },
            {
                "icon": "ri-file-list-3-line",
                "title": "Midela Teren",
                "link": ""
            },
            {
                "icon": "ri-price-tag-2-line",
                "title": "Pira Neve",
                "link": ""
            },

            {
                "icon": "ri-anchor-line",
                "title": "Dirada Pack",
                "link": ""
            },
            {
                "icon": "ri-disc-line",
                "title": "Moton Ideal",
                "link": ""
            },
            {
                "icon": "ri-base-station-line",
                "title": "Verdo Park",
                "link": ""
            },
            {
                "icon": "ri-fingerprint-line",
                "title": "Flavor Nivelanda",
                "link": ""
            }
        ],
        "events": [
            {
                "filename": "events-1",
                "link": "",
                "title": "Introduction to webdesign",
                "subtitle": "Sunday, September 26th at 7:00 pm",
                "desc": "Sed ut perspiciatis unde omnis iste natus error sit voluptatem doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo",
            },
            {
                "filename": "events-2",
                "link": "",
                "title": "Marketing Strategies",
                "subtitle": "Sunday, November 15th at 7:00 pm",
                "desc": "Lorem ipsum dolor sit amet, consectetur elit, sed do eiusmod tempor ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
            },
        ],
        "pricing": [
            {
                "featured": True,
                "advanced": False,
                "title": "1:1 Class",
                "price": "50000",
                "li": [
                    "1:1 - 1 hour (60 mins)",
                    "In-person or Zoom",
                    "Lesson note & Feedback"
                ],
                "disabled_li": [
                    "Pharetra massa",
                    "Massa ultricies mi"
                ],
                "link": {
                    "url": "#",
                    "title": "자세히보기"
                }
            },
            {
                "featured": True,
                "advanced": False,
                "title": "1:1 Class - 1.5h",
                "price": "70000",
                "li": [
                    "1:1 - 1.5 hour (90 mins)",
                    "In-person or Zoom",
                    "Lesson note & Feedback"
                ],
                "disabled_li": [
                    "Pharetra massa",
                    "Massa ultricies mi"
                ],
                "link": {
                    "url": "#",
                    "title": "자세히보기"
                }
            },
            {
                "featured": True,
                "advanced": False,
                "title": "1:1 Class - 2h",
                "price": "90000",
                "li": [
                    "1:1 - 2 hour (120 mins)",
                    "In-person or Zoom",
                    "Lesson note & Feedback"
                ],
                "disabled_li": [
                    "Pharetra massa",
                    "Massa ultricies mi"
                ],
                "link": {
                    "url": "#",
                    "title": "자세히보기"
                }
            },
            {
                "featured": False,
                "advanced": False,
                "title": "Group class",
                "price": "-",
                "li": [
                    "MyEnglish Circle",
                    "1 hour (60 mins)",
                    "Lesson note & Feedback",
                    "TBD"
                ],
                "disabled_li": [
                    "Zoom class"
                ],
                "link": {
                    "url": "#",
                    "title": "자세히보기"
                }
            }
        ],
    }

    context_kor = {
        "hero": {
            "bg": "bg1",
            "title": "말하고 이야기 하고",
            "slogan": "Global connection starts with improving your speaking skills<br>Let’s get to talking!",
            "btn": {"title": "Classes", "link": "#classes"}
        },

    }

    context_eng = {
        "hero": {
            "bg": "bg1",
            "title": "Say Tell Speak Talk",
            "slogan": "Global connection starts with improving your speaking skills<br>Let’s get to talking!",
            "btn": {"title": "Classes", "link": "#classes"}
        }
    }

    context_def = context_kor

    if lang == 'kor':
        context.update(context_kor)
    elif lang == 'eng':
        context.update(context_eng)
    else:
        context['lang']['selected'] = context['lang']['list'][0]
        context.update(context_def)

    counts_for_3 = {
        "counts": [
            ["fa-map-pin", "누적 임플란트 식립", 17862],
            ["fa-thumbs-up", "누적 교정 케이스", 3345],
            ["fa-user-md", "의료진", 3],
            ["fa-tooth", "누적 사랑니 발치", 16678]
        ]
    }
    counts_for_2 = {
        "counts": [
            ["학생", 17],
            ["클래스", 4],
            ["이벤트", 3],
            ["교사", 1]
        ]
    }

    if context['theme'] == 'medilab_ds' or context['theme'] == 'bethany_ds':
        context.update(counts_for_3)
    else:
        context.update(counts_for_2)

    logger.debug(context)

    if request.method == 'GET':
        return render(request, f"home/home.html", context)
    elif request.method == "POST":
        context.update(make_post_context(request.POST, 'hj3415@gmail.com'))
        return render(request, f"home/home.html", context)
