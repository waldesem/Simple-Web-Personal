<script setup lang="ts">
import { shallowRef } from "vue";
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elements";

// Определяем данные которые передаются через router из HomePage.vue
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const fullname = shallowRef("");
</script>

<template>
  <NUContainer>
    <NUPageHeader :title="fullname" />
    <NUPageBody>
      <NUTabs :items="[anketaTab, ...itemsTabs]" :unmount-on-hide="false">
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <PersonView
            :person-id="props.id"
            @listnames="(value: string[]) => (fullname = value.join(' '))"
          />
          <NUSeparator />
          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <NUAccordion :items="itemsAccordion">
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
          </NUAccordion>
        </template>
        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in itemsTabs" #[tab.slot] :key="tab.slot">
          <ItemView :cand-id="props.id" :title="tab.label" :view="tab.slot" />
        </template>
      </NUTabs>
    </NUPageBody>
  </NUContainer>
</template>
