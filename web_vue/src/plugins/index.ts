import ky from "ky";
import { App } from "vue";
import { useRouter } from "vue-router";
import { access, refresh } from "@/state";

export const api = {
  install(app: App) {
    const instanceKy = ky.create({
      hooks: {
        beforeRequest: [
          ({ request }) => {
            request.headers.set("Authorization", `Bearer ${access.value}`);
          },
        ],
        afterResponse: [
          async ({ request, response, retryCount }) => {
            if (response.status === 401 && retryCount === 0) {
              request.headers.set(
                "Authorization",
                `Bearer ${refresh.value}`,
              );
              const resp = await ky.post("/routes/auth/refresh");
              access.value = await resp.text();
              const headers = new Headers(request.headers);
              headers.set("Authorization", `Bearer ${access.value}`);

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
