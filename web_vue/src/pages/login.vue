<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useRouter } from "vue-router";
import type { FormSubmitEvent } from "@nuxt/ui";
import { useAlert } from "@/composables";
import { auth, validate } from "@/schema/forms";
import type { Auth, Login } from "@/types";

const router = useRouter();

const alerts = useAlert();

// Объявляем переменные для формы и состояния
const method = ref<"POST" | "PATCH">("POST");

// Объявляем функцию для отправки формы
async function onSubmit(payload: FormSubmitEvent<Partial<Login>>) {
  const resp = await ky("/routes/auth/login", {
    method: method.value,
    json: payload.data,
  }).catch((error) => {
    if (error.data.status_code === 401) {
      alerts.create(
        "error",
        "Неправильный логин или пароль. Попробуйте еще раз.",
      );
    } else console.error(error.data);
    alerts.create("error", "Ошибка соединения с сервером.");
  });
  if (resp?.status === 200) {
    method.value = "POST";
    alerts.create(
      "success",
      "Пароль успешно изменен. Войдите с новым паролем.",
    );
  } else if (resp?.status === 201) {
    const { message } = (await resp.json()) as Auth;
    if (message === "success") {
      return router.push("/persons");
    } else {
      alerts.create("warning", "Пароль просрочен. Измените пароль.");
      method.value = "PATCH";
    }
  } else {
    alerts.create(
      "error",
      "Неправильный логин или пароль. Попробуйте еще раз.",
    );
  }
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
        <UAlert
          variant="subtle"
          :icon="alerts.alert.value?.icon"
          :color="alerts.alert.value?.color"
          :title="alerts.alert.value?.title"
          :description="alerts.alert.value?.description"
        />
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
                alerts.create('info', 'Введите новый пароль и подтверждение.');
              } else {
                method = 'POST';
                alerts.create('success', 'Введите логин и пароль');
              }
            }
          "
        />
      </template>
    </UAuthForm>
  </UPageCard>
</template>
