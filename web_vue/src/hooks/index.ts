import ky from "ky";
import { useRouter } from "vue-router";
import { access, refresh } from "@/state";
import { Auth } from "@/types";

const { push } = useRouter();

export const api = ky.extend({
  hooks: {
    beforeRequest: [
      async ({ request }) => {
        if (access.value) {
          request.headers.set("Authorization", "Bearer " + access.value);
        } else {
          if (refresh.value) {
            const { access_token } = await ky
              .post<Auth>("/api/auth/refresh", { json: refresh.value })
              .json();
            request.headers.set("Authorization", "Bearer " + access_token);
            access.value = access_token;
          } else push("login");
        }
      },
    ],
    afterResponse: [
      async ({ request, response, retryCount }) => {
        if (!response.ok) {
          if (response.status === 401 && retryCount === 0) {
            const { access_token } = await ky
              .post<Auth>("/api/auth/refresh", { json: refresh.value })
              .json();

            const headers = new Headers(request.headers);
            headers.set("Authorization", `Bearer ${access_token}`);
            access.value = access_token;

            return ky.retry({
              request: new Request(request, { headers }),
            });
          }
          push("login");
        }
      },
    ],
  },
});
