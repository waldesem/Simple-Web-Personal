<script setup lang="ts">
import ky from "ky";
import { shallowRef } from "vue";
import { useAsyncState } from "@vueuse/core";
import { user as userItem } from "@/schema/items";
import { formUser } from "@/schema/forms";
import { userCols } from "@/schema/elems";
import { Actions, type User } from "@/types";

definePage({ meta: { layout: "AdminLayout" } });

// Определяем переменные для работы с данными
const content = shallowRef<"form" | "item">("form");
const method = shallowRef<"POST" | "PATCH">("POST");
const modal = shallowRef(false);
const user = shallowRef({} as User);

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
  <UContainer>
    <UPageHeader
      title="ПОЛЬЗОВАТЕЛИ"
      :ui="{ title: 'text-2xl sm:text-3xl text-gray-600' }"
    >
      <template #links>
        <UModal v-model:open="modal" title="Пользователь">
          <UButton
            icon="i-mi-user-add"
            :loading="isLoading"
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
              :fields="userItem"
              @update="method = 'PATCH'"
            >
              <div class="flex flex-wrap gap-2">
                <UButton
                  color="error"
                  variant="outline"
                  :label="user.deleted ? 'Восстановить' : 'Удалить'"
                  @click="edit(Actions.delete)"
                />
                <UButton
                  color="neutral"
                  variant="outline"
                  :label="user.blocked ? 'Разблокировать' : 'Заблокировать'"
                  @click="edit(Actions.block)"
                />
                <UButton
                  color="warning"
                  variant="outline"
                  label="Сбросить пароль"
                  @click="edit(Actions.reset)"
                />
              </div>
            </ItemDiv>
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <UPageBody>
      <TableDiv
        :cols="userCols"
        :data="state"
        @select="
          (row: User) => {
            content = 'item';
            user = row;
            modal = true;
          }
        "
      />
    </UPageBody>
  </UContainer>
</template>
