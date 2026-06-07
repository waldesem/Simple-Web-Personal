import ky from "ky";
import { useRouter } from "vue-router";

export const api = ky.create({
  hooks: {
    afterResponse: [
      async ({ request, response, retryCount }) => {
        if (!response.ok) {
          if (retryCount === 0) {
            const headers = new Headers(response.headers);
            headers.set("X-Retry-Count", retryCount.toString());
            return ky.retry({
              request: new Request(request, { headers }),
            });
          } else {
            const router = useRouter();
            router.replace({
              name: "error",
              params: {
                statusCode: response.status,
                statusMessage: response.statusText,
              },
            });
          }
        }
      },
    ],
  },
});
