export interface InfoData {
  className: string
  text: string
  url: string
  unit: typeof Units[keyof typeof Units] | null
}

export const Units = {
  kcal: 'kcal',
  Liter: 'L',
} as const;
