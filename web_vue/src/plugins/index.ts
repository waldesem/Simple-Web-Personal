import ky, { KyInstance } from "ky";
import { useRouter } from "vue-router";
import { accessToken, refreshToken } from "@/state";

export const ApiPlugin = {
  install(
    app: { config: { globalProperties: { $api: KyInstance } } },
    options: { baseURL: any },
  ) {
    const api = ky.create({
      baseUrl: options?.baseURL || "http://127.0.0.1:5000/api/",
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
              router.replace({ name: "login" });
            }
          },
        ],
      },
    });
    app.config.globalProperties.$api = api;
  },
};
