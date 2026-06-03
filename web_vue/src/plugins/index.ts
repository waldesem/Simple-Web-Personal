import ky from "ky";
import { App } from "vue";
import { useRouter } from "vue-router";
import { accessToken, refreshToken } from "@/state";

export const api = {
  install(app: App) {
    const instanceKy = ky.create({
      hooks: {
        beforeRequest: [
          ({ request }) => {
            request.headers.set("Authorization", `Bearer ${accessToken.value}`);
          },
        ],
        afterResponse: [
          async ({ request, response, retryCount }) => {
            if (response.status === 401 && retryCount === 0) {
              request.headers.set(
                "Authorization",
                `Bearer ${refreshToken.value}`,
              );
              const response = await ky.post("/routes/auth/refresh");
              accessToken.value = await response.text();
              const headers = new Headers(request.headers);
              headers.set("Authorization", `Bearer ${accessToken.value}`);

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
          },
        ],
      },
    });
    app.config.globalProperties.$api = instanceKy;
  },
};
