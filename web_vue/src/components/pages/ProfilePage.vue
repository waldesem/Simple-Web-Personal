<script setup lang="ts">
import { computed, onMounted, ref, shallowRef } from "vue";
import { ofetch } from "ofetch";
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elements";
import { itemsFields } from "@/schema/items";
import type { Person } from "@/types";

// Определяем данные которые передаются через router из HomePage.vue
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const data = shallowRef({} as Person);
const flag = ref(false);
const loading = ref(false); // ← триггер для анимации

onMounted(() => getPerson());

// Определяем функцию для получения данных из API
async function getPerson() {
  loading.value = true;
  data.value = await ofetch<Person>("/routes/persons/" + props.id);
  loading.value = false;
}

const fullname = computed(
  () =>
    `${data.value.surname ?? ""} ${data.value.firstname ?? ""} ${
      data.value.patronymic ?? ""
    }`,
);
</script>

<template>
  <UContainer>
    <UPageHeader :title="fullname">
      <template #links>
        <UButton
          :color="flag ? 'success' : 'error'"
          :icon="flag ? 'i-lucide-pencil' : 'i-lucide-pencil-off'"
          :title="flag ? 'Откл.Редакт.' : 'Вкл.Редакт.'"
          @click="flag = !flag"
        />
      </template>
    </UPageHeader>

    <UPageBody>
      <UTabs
        :items="[anketaTab, ...itemsTabs]"
        :unmount-on-hide="false"
        variant="pill"
      >
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <SkeletDivs v-if="loading" :rows="itemsFields.person.length" />
          <PersonView v-else :flag="flag" :person="data" @update="getPerson" />

          <USeparator />

          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <UAccordion :items="itemsAccordion" :unmount-on-hide="false">
            <template
              v-for="accord in itemsAccordion"
              #[accord.slot]
              :key="accord.slot"
            >
              <ItemView
                :cand-id="props.id"
                :flag="flag"
                :title="accord.label"
                :view="accord.slot"
              />
            </template>
          </UAccordion>
        </template>

        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in itemsTabs" #[tab.slot] :key="tab.slot">
          <ItemView
            :cand-id="props.id"
            :flag="flag"
            :title="tab.label"
            :view="tab.slot"
          />
        </template>
      </UTabs>
    </UPageBody>
  </UContainer>
</template>
