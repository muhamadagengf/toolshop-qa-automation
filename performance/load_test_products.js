import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * Logique QA Assessment - Bagian 4 (Bonus): Performance Test with k6
 * Target: Practice Software Testing API (GET /products)
 * 
 * Execution parameters:
 * - VUs: 10 - 20 Virtual Users
 * - Duration: ~1 minute
 * - Thresholds: p(95) < 1500ms, avg < 800ms, error rate < 1%
 * 
 * Run command:
 *   k6 run performance/load_test_products.js
 * Or via Docker:
 *   docker run --rm -i grafana/k6 run - < performance/load_test_products.js
 */

export const options = {
  stages: [
    { duration: '15s', target: 10 }, // Ramp up to 10 VUs
    { duration: '30s', target: 20 }, // Sustain load at 20 VUs
    { duration: '15s', target: 0 },  // Ramp down to 0 VUs
  ],
  thresholds: {
    // 95% of requests must complete below 1.5s; average below 800ms
    http_req_duration: ['p(95)<1500', 'avg<800'],
    // Error rate must be strictly below 1%
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_API_URL = __ENV.API_URL || 'https://api.practicesoftwaretesting.com';

export default function () {
  const url = `${BASE_API_URL}/products`;
  const params = {
    headers: {
      'Accept': 'application/json',
      'User-Agent': 'Logique-QA-k6-PerformanceTest/1.0',
    },
    tags: { name: 'GetProductsList' },
  };

  const response = http.get(url, params);

  // Validate response code and body structure
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response has data': (r) => {
      try {
        const body = JSON.parse(r.body);
        return Array.isArray(body.data) && body.data.length > 0;
      } catch (e) {
        return false;
      }
    },
    'response time < 1000ms': (r) => r.timings.duration < 1000,
  });

  // Realistic user pacing between product catalog browsing
  sleep(1);
}
