<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAlert } from "@/composables";
import { access, refresh } from "@/state";
import { auth, validate } from "@/schema/forms";
import type { FormSubmitEvent } from "@nuxt/ui";
import type { Auth, Login, Register } from "@/types";

const router = useRouter();

const { alert, update } = useAlert();

// Объявляем переменные для формы и состояния
const method = ref<"post" | "patch">("post");

// Объявляем функцию для отправки формы
async function onSubmit(payload: FormSubmitEvent<Partial<Register | Login>>) {
  const resp = await ky("/auth/login", {
    baseUrl: "/api",
    method: method.value,
    json: payload.data,
  });
  if (resp.ok) {
    const { message, access_token, refresh_token } =
      (await resp.json()) as Auth;
    if (message === "success") {
      access.value = access_token;
      refresh.value = refresh_token;
      return router.push("/");
    } else if (message === "denied") {
      update("warning", "Требуется смена пароля.");
      method.value = "patch";
    } else if (message === "updated") {
      method.value = "post";
      update("success", "Пароль изменен. Войдите с новым паролем.");
    } else update("error", "Неправильный логин или пароль");
  } else update();
}
</script>

<template>
  <UPageCard class="w-full max-w-md m-auto my-[20vh]">
    <UAuthForm
      icon="i-mi-lock"
      title="Вход в систему"
      description="Доступ в систему кадровой безопасности."
      :validate="validate[method]"
      :fields="auth[method]"
      :submit="{
        label: method === 'post' ? 'Войти' : 'Изменить',
        color: 'success',
        variant: 'outline',
      }"
      :ui="{ leadingIcon: 'text-blue-800' }"
      @submit.prevent="onSubmit($event)"
    >
      <template #validation>
        <UAlert variant="subtle" v-bind="{ ...alert }" />
      </template>
      <template #footer>
        <UButton
          :label="method == 'post' ? 'Изменить' : 'Отмена'"
          color="secondary"
          variant="outline"
          block
          @click="
            () => {
              if (method == 'post') {
                method = 'patch';
                update('info', 'Введите новый пароль и подтверждение.');
              } else {
                method = 'post';
                update('success', 'Введите логин и пароль');
              }
            }
          "
        />
      </template>
    </UAuthForm>
  </UPageCard>
</template>
