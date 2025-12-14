import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '30s', target: 10 },
        { duration: '1m', target: 50 },
        { duration: '1m', target: 100 },
        { duration: '30s', target: 0 },
    ],
    thresholds: {
        http_req_failed: ['rate<0.01'],
        http_req_duration: ['p(95)<1000'],  // 95% < 1s
    },
};

const BASE_URL = 'http://localhost:8000';

export default function () {

    // GET /
    const resRoot = http.get(`${BASE_URL}/`);
    check(resRoot, {
        'GET / -> status 200': (r) => r.status === 200,
    });

    // GET /db_health
    const resHealth = http.get(`${BASE_URL}/db_health`);
    check(resHealth, {
        'GET /db_health -> status 200': (r) => r.status === 200,
    });

    // POST /user/login
    const payload_login = JSON.stringify({
        telegram_id: 'telegram_123',
    });

    const params_login = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const resLogin = http.post(`${BASE_URL}/user/login`, payload_login, params_login);
    check(resLogin, {
        'POST /user/login -> success': (r) =>
            r.status === 200 || r.status === 401 || r.status === 403,
    });

    // PUT /user/update_info
    const payload_update_info = JSON.stringify({
        "id": "06b598b9-843f-459f-a5db-592a79c46404",
        "name": "Denys",
        "lastname": "Ponomarenko",
        "birthday": "2005-01-06",
        "weight": 100,
        "height": 182,
        "sex": "m",
        "count_of_sport_in_week": 3,
        "goal": 0
    });

    const params_update_info = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const resUpdate = http.put(`${BASE_URL}/user/update_info`, payload_update_info, params_update_info);
    check(resUpdate, {
        'PUT /user/update_info -> success': (r) => r.status === 202,
    });

    sleep(1);
}
