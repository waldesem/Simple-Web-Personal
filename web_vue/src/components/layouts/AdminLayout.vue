<template>
  <UPage>
    <UHeader v-once to="/users">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div>ADMIN</div>
          <div>STAFFSEC</div>
        </div>
      </template>
      <template #default>
        <UButton
          active-class="font-bold"
          inactive-class="text-muted"
          color="neutral"
          icon="i-mi-users"
          label="Кандидаты"
          to="/"
          variant="link"
        />
      </template>
      <template #right>
        <UAvatar text="A" :chip="{ inset: true, color: 'secondary' }" />
      </template>
    </UHeader>
    <UMain>
      <slot />
    </UMain>
    <UFooter v-once />
  </UPage>
</template>
