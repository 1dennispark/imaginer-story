
export const MAX_IMAGE_LIST_LENGTH = 10;
export const MIN_IMAGE_LIST_LENGTH = 6;
export const MAX_PRESET_LIST_LENGTH = 4;
export const MAX_SELECTED_PRESET_LENGTH = 2;

export const MBTI_ITEMS = [
    {label : 'INFJ', value: 'INFJ'},
    {label : 'INFP', value: 'INFP'},
    {label : 'ISFJ', value: 'ISFJ'},
    {label : 'ISFP', value: 'ISFP'},
    {label : 'ISTP', value: 'ISTP'},
    {label : 'ISTJ', value: 'ISTJ'},
    {label : 'INTP', value: 'INTP'},
    {label : 'INTJ', value: 'INTJ'},
    {label : 'ENTP', value: 'ENTP'},
    {label : 'ESTJ', value: 'ESTJ'},
    {label : 'ESTP', value: 'ESTP'},
    {label : 'ENFP', value: 'ENFP'},
    {label : 'ESFJ', value: 'ESFJ'},
    {label : 'ENTJ', value: 'ENTJ'},
    {label : 'ENFJ', value: 'ENFJ'},
    {label : 'ESFP', value: 'ESFP'},
];

export const AGE_RANGE_ITEMS = [
    {label : '10대', value: '10대'},
    {label : '20~30대', value: '20~30대'},
    {label : '30~40대', value: '30~40대'},
    {label : '40~50대', value: '40~50대'},
    {label : '60대 이상', value: '60대 이상'},
];

export const JOB_ITEMS = [
    {label : '군인', value: '군인'},
    {label : '마법사', value: '마법사'},
    {label : '우주비행사', value: '우주비행사'},
    {label : '소방관', value: '소방관'},
    {label : '경찰', value: '경찰'},
    {label : '게임 전사', value: '게임 전사'},
    {label : '축구 선수', value: '축구 선수'},
    {label : '배우', value: '배우'},
];

export const GENDER_ITEMS = [
    {label : '남자', value: '남자'},
    {label : '여자', value: '여자'},
];

export const BACKDROP_ITEMS = [
    {label : '우주', value: 'space'},
    {label : '숲', value: 'forest'},
    {label : '바다', value: 'the sea'},
    {label : '산', value: 'mountain'},
    {label : '도시', value: 'city'},
    {label : '호수', value: 'lake'},
    {label : '평야', value: 'the plain'},
    {label : '섬', value: 'island'},
];

export const GENRE_ITEMS = [
    {label : '액션', value: 'action'},
    {label : '드라마', value: 'drama'},
    {label : '코미디', value: 'comedy'},
    {label : '로맨스', value: 'romance'},
    {label : '판타지', value: 'fantasy'},
    {label : '스릴러', value: 'thriller'},
    {label : '공포', value: 'horror'},
    {label : '미스터리', value: 'mystery'},
    {label : '범죄', value: 'crime'},
    {label : 'SF', value: 'sf'},
    {label : '다큐멘터리', value: 'documentary'},
    {label : '가족', value: 'family'},
    {label : '전쟁', value: 'war'},
    {label : '역사', value: 'history'},
    {label : '음악', value: 'music'},
    {label : '서부', value: 'western'},
];

export const ENDING_ITEMS = [
    {label : '해피엔딩', value: 'happyending'},
    {label : '새드엔딩', value: 'sadending'},
];

export const API_URL = function () {
    if (process.env.NODE_ENV === 'production') {
        return '/v1';
    } else {
        return 'http://localhost:8080/v1';
    }
}()