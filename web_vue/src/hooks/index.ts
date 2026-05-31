import ky from "ky";
import { useRouter } from "vue-router";
import { accessToken, refreshToken } from "@/state";

export const api = ky.create({
  hooks: {
    beforeRequest: [
      ({ request }) => {
        request.headers.set("Authorization", `Bearer ${accessToken}`);
      },
    ],
    afterResponse: [
      async ({ request, response, retryCount }) => {
        if (response.status === 401 && retryCount === 0) {
          request.headers.set("Authorization", `Bearer ${refreshToken}`);
          const response = await ky.post("routes/auth/refresh");
          accessToken.value = await response.text();
          const headers = new Headers(request.headers);
          headers.set("Authorization", `Bearer ${accessToken.value}`);

          return ky.retry({
            request: new Request(request, { headers }),
          });
        } else {
          const router = useRouter();
          router.replace({ name: "login" });
        }
      },
    ],
  },
});
