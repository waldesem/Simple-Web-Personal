<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useAsyncState } from "@vueuse/core";
import { formUser } from "@/schema/forms";
import { userCols, userDivs } from "@/schema/users";
import { Actions, type User } from "@/types";

// Определяем переменные для работы с данными
const content = ref<"form" | "item">("form");
const method = ref<"POST" | "PATCH">("POST");
const modal = ref(false);
const user = ref({} as User);

const { execute, isLoading, state } = useAsyncState<User[]>(
  async () => await ky.get("/api/users/").json(),
  [],
);

// Объявляем функцию для действия с пользователем
async function edit(action: Actions) {
  if (!confirm("Подтвердить действие?")) return;
  const resp = await ky.post("/api/users/" + user.value.id, {
    json: { actions: action },
  });
  if (resp?.status == 201 || resp?.status == 200) {
    await execute();
    alert("Действие успешно выполнено");
  } else alert("Невозможно выполнить действие!");
}

async function submit(form: User) {
  modal.value = false;
  const url =
    "/api/users" + (method.value === "POST" ? "/" : "/" + user.value.id);
  const resp = await ky(url, { method: method.value, json: form });
  if (resp.status === 201) {
    await execute();
    alert("Пользователь успешно добавлен");
  } else alert("Невозможно выполнить действие!");
}
</script>

<template>
  <NUContainer>
    <NUPageHeader title="ПОЛЬЗОВАТЕЛИ" :ui="{ title: 'text-gray-600' }">
      <template #links>
        <NUModal v-model:open="modal" title="Пользователь">
          <NUButton
            icon="i-mi-user-add"
            :disabled="isLoading"
            size="lg"
            title="Добавить пользователя"
            variant="ghost"
            @click="
              content = 'form';
              method = 'POST';
              modal = true;
              user = {} as User;
            "
          />
          <template #body>
            <FormDiv
              v-if="content === 'form'"
              :fields="formUser"
              :item="user"
              @submit="submit"
            />
            <ItemDiv
              v-else
              :item="user"
              :fields="userDivs"
              @update="method = 'PATCH'"
            >
              <div class="flex flex-wrap gap-2">
                <NUButton
                  color="error"
                  variant="outline"
                  :label="user.deleted ? 'Восстановить' : 'Удалить'"
                  @click="edit(Actions.delete)"
                />
                <NUButton
                  color="neutral"
                  variant="outline"
                  :label="user.blocked ? 'Разблокировать' : 'Заблокировать'"
                  @click="edit(Actions.block)"
                />
                <NUButton
                  color="warning"
                  variant="outline"
                  label="Сбросить пароль"
                  @click="edit(Actions.reset)"
                />
              </div>
            </ItemDiv>
          </template>
        </NUModal>
      </template>
    </NUPageHeader>

    <NUPageBody>
      <TableDiv
        :class="{ 'animate-pulse': isLoading }"
        :cols="userCols"
        :data="state"
        @select="
          (row: User) => {
            content = 'item';
            modal = true;
            user = row;
          }
        "
      />
    </NUPageBody>
  </NUContainer>
</template>
