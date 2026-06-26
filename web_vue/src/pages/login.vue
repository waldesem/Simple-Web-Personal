<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useRouter } from "vue-router";
import type { FormSubmitEvent } from "@nuxt/ui";
import { useAlert } from "@/composables";
import { access, refresh } from "@/state";
import { auth, validate } from "@/schema/forms";
import type { Auth, Login } from "@/types";

const { push } = useRouter();

const { alert, update } = useAlert();

// Объявляем переменные для формы и состояния
const method = ref<"POST" | "PATCH">("POST");

// Объявляем функцию для отправки формы
async function onSubmit(payload: FormSubmitEvent<Partial<Login>>) {
  const resp = await ky("/routes/auth/login", {
    method: method.value,
    json: payload.data,
  });
  if (resp.ok) {
    const { message, access_token, refresh_token } =
      (await resp.json()) as Auth;
    if (message === "success") {
      access.value = access_token;
      refresh.value = refresh_token;
      return push("/index");
    } else if (message === "denied") {
      update("warning", "Требуется смена пароля.");
      method.value = "PATCH";
    } else if (message === "updated") {
      method.value = "POST";
      update("success", "Пароль изменен. Войдите с новым паролем.");
    } else update("error", "Неправильный логин или пароль");
  } else update();
}
</script>

<template>
  <UPageCard class="w-full max-w-md m-auto my-[20vh]">
    <UAuthForm
      description="Доступ в систему кадровой безопасности."
      icon="i-mi-lock"
      :validate="validate[method]"
      :fields="auth[method]"
      :submit="{
        label: method === 'POST' ? 'Войти' : 'Изменить',
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
          :label="method == 'POST' ? 'Изменить' : 'Отмена'"
          color="secondary"
          variant="outline"
          block
          @click="
            () => {
              if (method == 'POST') {
                method = 'PATCH';
                update('info', 'Введите новый пароль и подтверждение.');
              } else {
                method = 'POST';
                update('success', 'Введите логин и пароль');
              }
            }
          "
        />
      </template>
    </UAuthForm>
  </UPageCard>
</template>
