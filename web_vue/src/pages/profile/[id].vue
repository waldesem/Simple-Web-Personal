<script setup lang="ts">
import { KyInstance } from "ky";
import { defineAsyncComponent, inject, ref } from "vue";
import { useAsyncState, useClipboard } from "@vueuse/core";
import { useToasts } from "@/composables";
import { accordion, person as personFields, tabs } from "@/schema/items";
import { person as PersonForm } from "@/schema/forms";
import type { ItemsArray, Person } from "@/types";

const PrintView = defineAsyncComponent(
  () => import("@/components/content/PrintView.vue"),
);

definePage({ meta: { layout: "user" }, props: true });

const { id: candId } = defineProps({
  id: { type: String, required: true }, // ID кандидата из persons.vue
});

const toast = useToast();

const { create } = useToasts(toast);

const { copy, copied } = useClipboard();

const api = inject("api") as KyInstance;

const modal = ref(false); // Объявляем переменную модального окна

const print = ref(false); // Переключатель печати

const itemsData = ref({} as ItemsArray); // Данные для печатной формы

const anketa = { label: "Анкета", icon: "i-lucide-user", slot: "person" };

const { execute, state, isLoading } = useAsyncState<Person>(
  async () => await api.get("persons/" + candId).json(),
  {} as Person,
);

// Определяем функцию для отправки данных формы на сервер
async function submit(form: Person) {
  modal.value = false;
  isLoading.value = true;
  const { ok } = await api.patch("persons/" + candId, {
    json: form,
  });
  await execute();
  if (ok) create("info", "Данные обновлены!");
  else {
    create();
    isLoading.value = false;
  }
}
</script>

<template>
  <KeepAlive exclude="PrintView">
    <UContainer v-if="print" class="relative">
      <PrintView :person="state" :datas="itemsData" v-model="print" />
    </UContainer>

    <UContainer v-else>
      <UPage>
        <UPageHeader
          :title="`${state.surname} ${state.firstname} ${state.patronymic ?? ''}`"
        >
          <template #links>
            <UButton
              icon="i-lucide-printer"
              variant="outline"
              @click="print = true"
            />
          </template>
        </UPageHeader>
        <UPageBody>
          <UTabs :items="[anketa, ...tabs]" :unmount-on-hide="true">
            <!-- Слот вкладки для отображения анкеты -->
            <template #person>
              <ItemDiv
                :class="{ 'animate-pulse': isLoading }"
                class="m-2"
                :fields="personFields"
                :item="state"
                @delete="null"
                @update="modal = true"
              >
                <template #destination>
                  <UButton
                    v-if="state?.destination"
                    :color="copied ? 'success' : 'info'"
                    :label="copied ? 'Скопировано' : 'Копировать'"
                    size="sm"
                    variant="outline"
                    @click="copy(state.destination)"
                  />
                </template>
              </ItemDiv>

              <!-- Модальное окно для редактирования данных -->
              <UModal
                v-model:open="modal"
                title="Aнкета"
                description="Редактирование анкетные данные"
              >
                <template #body>
                  <FormDiv
                    :fields="PersonForm"
                    :item="state"
                    @submit="submit"
                  />
                </template>
              </UModal>

              <USeparator />

              <!-- Aккордеон с данными staffs, educations и т.д. -->
              <UAccordion
                :items="accordion"
                :unmount-on-hide="false"
                class="mx-2"
              >
                <template
                  v-for="accord in accordion"
                  #[accord.slot]
                  :key="accord.slot"
                >
                  <ItemView
                    :cand-id="candId"
                    :title="accord.label"
                    :view="accord.slot"
                    @update="(event) => (itemsData[accord.slot] = event)"
                  />
                </template>
              </UAccordion>
            </template>

            <!-- Вкладки проверки, полиграф и др. -->
            <template v-for="tab in tabs" #[tab.slot] :key="tab.slot">
              <div class="m-2">
                <ItemView
                  :cand-id="candId"
                  :title="tab.label"
                  :view="tab.slot"
                  @update="(event) => (itemsData[tab.slot] = event)"
                />
              </div>
            </template>
          </UTabs>
        </UPageBody>
      </UPage>
    </UContainer>
  </KeepAlive>
</template>
