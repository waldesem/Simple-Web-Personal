<script setup lang="ts">
import ky from "ky";
import { h, ref, resolveComponent } from "vue";
import { shallowRef } from "vue";
import { useAsyncState } from "@vueuse/core";
import { TableColumn } from "@nuxt/ui";
import { localStr } from "@/utils";
import { user as userItem } from "@/schema/items";
import { user as formUser } from "@/schema/forms";
import { Actions, type User } from "@/types";

definePage({ meta: { layout: "AdminLayout" } });

// Определяем переменные для работы с данными
const expanded = ref({ 1: false });
const method = shallowRef<"POST" | "PATCH">("POST");
const modal = shallowRef(false);
const user = shallowRef({} as User);

const Button = resolveComponent("UButton");

const columns: TableColumn<User>[] = [
  {
    id: "expand",
    cell: ({ row }) =>
      h(Button, {
        color: "neutral",
        variant: "ghost",
        icon: "i-mi-chevron-down",
        square: true,
        ui: {
          leadingIcon: [
            "transition-transform",
            row.getIsExpanded() ? "duration-200 rotate-180" : "",
          ],
        },
        onClick: () => row.toggleExpanded(),
      }),
  },
  { accessorKey: "id", header: "#" },
  { accessorKey: "fullname", header: "Пользователь" },
  { accessorKey: "username", header: "Логин" },
  { accessorKey: "role", header: "Роль" },
  {
    accessorKey: "created",
    header: "Создан",
    cell: ({ row }) => localStr(row.original.created),
  },
];

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
            :loading="isLoading"
            color="neutral"
            icon="i-mi-user-add"
            size="lg"
            title="Добавить пользователя"
            variant="ghost"
            @click="
              method = 'POST';
              modal = true;
              user = {} as User;
            "
          />
          <template #body>
            <FormDiv :fields="formUser" :item="user" @submit="submit" />
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <UPageBody>
      <UTable
        v-model:expanded="expanded"
        class="flex-1"
        sticky
        :data="state"
        :columns="columns"
        :loading="isLoading"
        loading-animation="swing"
      >
        <template #expanded="{ row }">
          <UCard>
            <ItemDiv
              :item="row.original"
              :fields="userItem"
              @update="
                user = row.original;
                modal = true;
                method = 'PATCH';
              "
            >
              <UFieldGroup>
                <UButton
                  color="error"
                  variant="outline"
                  :label="row.original.deleted ? 'Восстановить' : 'Удалить'"
                  @click="edit(Actions.delete)"
                />
                <UButton
                  color="neutral"
                  variant="outline"
                  :label="
                    row.original.blocked ? 'Разблокировать' : 'Заблокировать'
                  "
                  @click="edit(Actions.block)"
                />
                <UButton
                  color="warning"
                  variant="outline"
                  label="Сбросить пароль"
                  @click="edit(Actions.reset)"
                />
              </UFieldGroup>
            </ItemDiv>
          </UCard>
        </template>
      </UTable>
    </UPageBody>
  </UContainer>
</template>
