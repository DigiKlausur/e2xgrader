export namespace NbgraderMetadata {
  export interface INbgraderMetadata {
    cell_type?: string;
    checksum?: string;
    solution: boolean;
    task: boolean;
    grade: boolean;
    grade_id: string;
    locked: boolean;
    points?: number;
    schema_version: number;
  }

  export const NBGRADER_METADATA_KEY = 'nbgrader';
  export const NBGRADER_SCHEMA_VERSION = 3;
  export function newNbGraderMetadata(): INbgraderMetadata {
    return {
      solution: false,
      task: false,
      grade: false,
      grade_id: `cell-${Private.randomString(12)}`,
      locked: false,
      schema_version: NBGRADER_SCHEMA_VERSION
    };
  }

  namespace Private {
    export function randomString(length: number): string {
      let result = '';
      const chars = 'abcdef0123456789';
      let i;
      for (i = 0; i < length; i++) {
        result += chars[Math.floor(Math.random() * chars.length)];
      }
      return result;
    }
  }
}

export enum NbgraderCellType {
  MANUALLY_GRADED_ANSWER = 'manual',
  AUTOGRADED_ANSWER = 'auto',
  TASK = 'task',
  AUTOGRADER_TEST = 'tests',
  DESCRIPTION = 'readonly'
}

export namespace NbgraderCellTypes {
  /**
   * Interface representing the information of a cell type.
   */
  interface ICellTypeInfo {
    /**
     * Partial metadata of the cell, adhering to the INbgraderMetadata interface.
     */
    metadata: Partial<NbgraderMetadata.INbgraderMetadata>;

    /**
     * Label associated with the cell type.
     */
    label: string;

    /**
     * Indicates whether only code cells are allowed for this cell type.
     */
    codeOnly: boolean;
  }

  const cellTypeInfo: Record<NbgraderCellType, ICellTypeInfo> = {
    [NbgraderCellType.DESCRIPTION]: {
      metadata: {
        solution: false,
        grade: false,
        task: false,
        locked: true
      },
      label: 'Read Only',
      codeOnly: false
    },
    [NbgraderCellType.MANUALLY_GRADED_ANSWER]: {
      metadata: {
        solution: true,
        grade: true,
        task: false,
        locked: false
      },
      label: 'Manually graded answer',
      codeOnly: false
    },
    [NbgraderCellType.AUTOGRADED_ANSWER]: {
      metadata: {
        solution: true,
        grade: false,
        task: false,
        locked: false
      },
      label: 'Autograded answer',
      codeOnly: true
    },
    [NbgraderCellType.AUTOGRADER_TEST]: {
      metadata: {
        solution: false,
        grade: true,
        task: false,
        locked: true
      },
      label: 'Autograder tests',
      codeOnly: true
    },
    [NbgraderCellType.TASK]: {
      metadata: {
        solution: false,
        grade: false,
        task: true,
        locked: true
      },
      label: 'Task',
      codeOnly: false
    }
  };

  export const NBGRADER_MARKDOWN_CELL_TYPES = Object.values(
    NbgraderCellType
  ).filter(type => !cellTypeInfo[type].codeOnly);
  export const NBGRADER_CODE_CELL_TYPES = Object.values(NbgraderCellType);

  export const cellTypeConfigurations = Object.fromEntries(
    Object.entries(cellTypeInfo).map(([key, { metadata }]) => [key, metadata])
  ) as Record<NbgraderCellType, Partial<NbgraderMetadata.INbgraderMetadata>>;

  export const cellTypeLabels = Object.fromEntries(
    Object.entries(cellTypeInfo).map(([key, { label }]) => [key, label])
  ) as Record<NbgraderCellType, string>;

  /**
   * Finds the matching cell type based on the provided grading metadata.
   *
   * @param metadata - The grading metadata to match against cell type configurations.
   * @returns The matching Nbgrader cell type if a match is found, otherwise undefined.
   */
  export function findMatchingCellType(
    metadata: NbgraderMetadata.INbgraderMetadata | undefined
  ): NbgraderCellType | undefined {
    for (const [type, config] of Object.entries(cellTypeConfigurations)) {
      if (Private.metadataMatchesConfig(metadata, config)) {
        return type as NbgraderCellType;
      }
    }
    return undefined;
  }

  /**
   * Checks if the given cell metadata matches the specified cell type.
   *
   * @param metadata - The metadata of the cell, which may be undefined.
   * @param cellType - The type of the cell to check against.
   * @returns A boolean indicating whether the cell metadata matches the specified cell type.
   */
  export function matchesCellType(
    metadata: NbgraderMetadata.INbgraderMetadata | undefined,
    cellType: NbgraderCellType
  ): boolean {
    return Private.metadataMatchesConfig(
      metadata,
      cellTypeInfo[cellType].metadata
    );
  }

  namespace Private {
    export function metadataMatchesConfig(
      metadata: NbgraderMetadata.INbgraderMetadata | undefined,
      config: Partial<NbgraderMetadata.INbgraderMetadata>
    ): boolean {
      return Object.entries(config).every(([key, value]) => {
        return (
          metadata?.[key as keyof NbgraderMetadata.INbgraderMetadata] === value
        );
      });
    }
  }
}
