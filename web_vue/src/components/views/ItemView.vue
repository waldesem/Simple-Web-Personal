<script setup lang="ts">
import { onMounted, type PropType, ref, shallowRef } from "vue";
import { ofetch } from "ofetch";
import { itemFields } from "@/schema/items";
import { formFields } from "@/schema/forms";
import type { Items } from "@/types";

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  flag: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  view: {
    type: String as PropType<keyof Items>,
    required: true,
  },
});

const data = shallowRef<Items[keyof Items][]>([]);
const item = shallowRef<Items[keyof Items]>({});
const loading = ref(false); // ← триггер для анимации
const modal = ref(false); // Флаг для открытия модального окна
const method = ref<"POST" | "PATCH">("POST");

onMounted(() => getItem());

// Определяем функцию для получения данных из API
async function getItem() {
  loading.value = true;
  data.value = await ofetch(`/routes/${props.view}/${props.candId}`);
  loading.value = false;
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
  item.value = ({} as typeof item.value);
  if (status !== 201 && status !== 200) alert("Невозможно выполнить действие!");
  await getItem();
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
  } else {
    alert("Невозможно выполнить действие!");
    loading.value = false;
  }
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty v-if="!data?.length" class="m-4" title="Данные отсутствуют" size="sm">
    <template #body>
      <UButton
        v-show="props.flag"
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

  <SkeletDivs v-if="loading && !data" :rows="itemFields[view].length" />

  <div
    v-for="(content, index) in data"
    :key="index"
    :class="{ 'animate-pulse': loading }"
    class="p-2 my-2"
  >
    <!-- Выводим кнопки редактирования/удаления данных, в режиме редактирования -->
    <DropMenu
      v-show="props.flag"
      @update="
        item = content;
        modal = true;
        method = 'PATCH';
      "
      @delete="deleteItem(content.id)"
    />
    <!-- Выводим элемент данных -->
    <ItemDiv :item="content" :fields="itemFields[view]" />
    <USeparator v-if="index + 1 < data.length" />
  </div>

  <!-- Модальное окно для редактирования данных -->
  <UModal
    v-model:open="modal"
    :title="props.title"
    description="Добавить/редактировать данные"
  >
    <UButton
      v-if="props.flag && data?.length"
      class="my-2"
      label="Добавить запись"
      variant="outline"
      size="sm"
      block
      @click="method = 'POST'"
    />
    <template #body>
      <FormDiv :item="item" :fields="formFields[view]" @submit="submitItem" />
    </template>
  </UModal>
</template>
