export const localStr = (data: string): string => {
  return data ? new Date(data).toLocaleDateString() : "";
};
