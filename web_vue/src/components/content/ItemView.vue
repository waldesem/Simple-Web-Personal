<script setup lang="ts">
import { onMounted, PropType, ref, shallowRef } from "vue";
import { ofetch } from "ofetch";
import { flag } from "@/utils";
import { itemFields } from "@/schema/items";
import { formFields } from "@/schema/forms";
import type { Items } from "@/types";

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  view: {
    type: String as PropType<keyof Items>,
    required: true,
  },
  candId: {
    type: String,
    required: true,
  },
});

const data = shallowRef<Items[keyof Items]>([]);
const item = shallowRef({} as (typeof data.value)[number]);
const modal = ref(false); // Флаг для открытия модального окна
const method = ref<"POST" | "PATCH">("POST");
const loading = ref(false); // ← триггер для анимации

onMounted(() => getItem());

// Определяем функцию для получения данных из API
async function getItem() {
  data.value = await ofetch(`/routes/${props.view}/${props.candId}`);
}

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  loading.value = true;
  const url = `/routes/${props.view}/${props.candId}`;
  const { status } = await ofetch.raw(
    method.value === "POST" ? url : `${url}/${item.value.id}`,
    {
      method: method.value,
      body: form,
    },
  );
  if (status !== 201 && status !== 200) alert("Невозможно выполнить действие!");
  item.value = {} as (typeof data.value)[number];
  await getItem();
  loading.value = false;
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  loading.value = true;
  const { status } = await ofetch.raw(`/routes/${props.view}/${itemId}`, {
    method: "DELETE",
  });
  if (status === 204) {
    await getItem();
    loading.value = false;
  } else {
    alert("Невозможно выполнить действие!");
  }
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty v-if="!data?.length" class="m-4" title="Данные отсутствуют" size="sm">
    <template #body>
      <UButton
        v-show="flag"
        label="Добавить запись"
        variant="outline"
        size="sm"
        @click="
          modal = true;
          method = 'POST';
        "
      />
    </template>
  </UEmpty>

  <div
    v-for="(content, index) in data"
    :key="index"
    :class="{ 'animate-pulse': loading }"
    class="p-2 my-2"
  >
    <!-- Выводим кнопки редактирования/удаления данных, в режиме редактирования -->
    <DivMenu
      v-show="flag"
      @update="
        item = content;
        modal = true;
        method = 'PATCH';
      "
      @delete="deleteItem(content.id)"
    />
    <!-- Выводим элемент данных -->
    <ItemCard :item="content" :fields="itemFields[view]" />
    <USeparator v-if="index + 1 < data.length" />
  </div>

  <!-- Модальное окно для редактирования данных -->
  <UModal
    v-model:open="modal"
    :title="props.title"
    description="Добавить/редактировать данные"
  >
    <UButton
      v-if="flag && data?.length"
      class="my-2"
      label="Добавить запись"
      variant="outline"
      size="sm"
      block
      @click="method = 'POST'"
    />
    <template #body>
      <FormCard :item="item" :fields="formFields[view]" @submit="submitItem" />
    </template>
  </UModal>
</template>
