import ky from "ky";
import { access, refresh } from "@/state";
import { router } from "@/router";
import { Auth } from "@/types";

export const api = ky.extend({
  baseUrl: "/api/",
  hooks: {
    beforeRequest: [
      async ({ request }) => {
        if (access.value) {
          request.headers.set("Authorization", "Bearer " + access.value);
        } else {
          if (refresh.value) {
            try {
              const { access_token } = await ky
                .post<Auth>("auth/refresh", { json: { token: refresh.value } })
                .json();
              request.headers.set("Authorization", "Bearer " + access_token);
              access.value = access_token;
            } catch (error) {
              router.push("/login");
            }
          } else {
            router.push("/login");
          }
        }
      },
    ],
    afterResponse: [
      async ({ request, response, retryCount }) => {
        if (!response.ok) {
          if (response.status === 401 && retryCount === 0) {
            try {
              const { access_token } = await ky
                .post<Auth>("auth/refresh", { json: { token: refresh.value } })
                .json();

              const headers = new Headers(request.headers);
              headers.set("Authorization", `Bearer ${access_token}`);
              access.value = access_token;

              return ky.retry({
                request: new Request(request, { headers }),
              });
            } catch (error) {
              router.push("/login");
            }
          } else if (response.status >= 400 && response.status < 500)
            router.push("/login");
        }
      },
    ],
  },
});
