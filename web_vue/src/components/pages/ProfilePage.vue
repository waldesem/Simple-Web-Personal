<script setup lang="ts">
import { shallowRef } from "vue";
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elems";

// Определяем данные которые передаются через router из HomePage.vue
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});
// Определяем переменную для UPageHeader
const fullname = shallowRef("");
</script>

<template>
  <UContainer>
    <UPageHeader :title="fullname" />
    <UPageBody>
      <UTabs :items="[anketaTab, ...itemsTabs]" :unmount-on-hide="false">
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <PersonView
            :person-id="props.id"
            @listnames="(value: string[]) => (fullname = value.join(' '))"
          />
          <USeparator />
          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <UAccordion :items="itemsAccordion">
            <template
              v-for="accord in itemsAccordion"
              #[accord.slot]
              :key="accord.slot"
            >
              <ItemView
                :cand-id="props.id"
                :title="accord.label"
                :view="accord.slot"
              />
            </template>
          </UAccordion>
        </template>
        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in itemsTabs" #[tab.slot] :key="tab.slot">
          <ItemView :cand-id="props.id" :title="tab.label" :view="tab.slot" />
        </template>
      </UTabs>
    </UPageBody>
  </UContainer>
</template>
