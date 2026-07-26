<script lang="ts">
import type { Items, Person } from "@/types";

type ToArray<T> = {
  [K in keyof T]: T[K][];
};

export interface ItemsArray extends ToArray<Items> {}
</script>

<script setup lang="ts">
import { KyInstance } from "ky";
import { inject, ref, resolveComponent } from "vue";
import { useAsyncState, useClipboard } from "@vueuse/core";
import { useToasts } from "@/composables";
import { accordion, person as personItem, tabs } from "@/schema/items";
import { person as personForm } from "@/schema/forms";

const UAccordion = resolveComponent("UAccordion");
const UTabs = resolveComponent("UTabs");

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
  ok ? create("info", "Данные обновлены!") : create();
}
</script>

<template>
  <UContainer>
    <UPage>
      <UPageHeader
        :title="`${state.surname} ${state.firstname} ${state.patronymic ?? ''}`"
        :ui="{
          root: print ? 'mt-0' : '',
          title: print ? 'text-xl text-gray-800' : '',
        }"
      >
        <template #links>
          <UButton
            class="no-print"
            :icon="print ? 'i-lucide-printer-x' : 'i-lucide-printer'"
            :color="print ? 'error' : 'primary'"
            :title="print ? 'Отмена' : 'Печать'"
            variant="outline"
            @click="print = !print"
          />
        </template>
      </UPageHeader>
      <UPageBody>
        <!--При печати переключаем табы на аккордион и раскрываем все элементы -->
        <KeepAlive>
          <component
            :is="print ? UAccordion : UTabs"
            :items="[anketa, ...tabs]"
            :unmount-on-hide="false"
            v-bind="{
              type: print ? 'multiple' : 'single',
              defaultValue: print
                ? accordion.map((_, idx) => String(idx))
                : undefined,
            }"
          >
            <!-- Слот вкладки для отображения анкеты -->
            <template #person>
              <ItemDiv
                :class="{ 'animate-pulse': isLoading }"
                class="m-2"
                :fields="personItem"
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
                    :fields="personForm"
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
                :type="print ? 'multiple' : 'single'"
                class="mx-2"
                :default-value="
                  print ? accordion.map((_, idx) => String(idx)) : undefined
                "
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
                />
              </div>
            </template>
          </component>
        </KeepAlive>
      </UPageBody>
    </UPage>
  </UContainer>
</template>

<style lang="css" scoped>
@media print {
  :deep(div[data-state="closed"]),
  :deep(.iconify) {
    display: none !important;
    visibility: hidden;
  }
  :deep(span[data-slot="label"]) {
    font-weight: bolder;
  }
}
</style>
